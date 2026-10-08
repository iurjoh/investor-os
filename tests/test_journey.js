/* Browser recovery contract, only bundled synthetic data.
 * Install tooling in a temporary folder (not the app):
 *   npm install --prefix /tmp/investor-qa @playwright/test@1.51.1
 *   /tmp/investor-qa/node_modules/.bin/playwright install chromium
 *   NODE_PATH=/tmp/investor-qa/node_modules node tests/test_journey.js
 * No live deployment, API, account or personal CSV is used.
 * "Restaurar visão" is a UI reset, NOT import/backup restoration.
 */
const {chromium}=require('@playwright/test');
const assert=require('node:assert/strict');
const {createServer}=require('node:http');
const fs=require('node:fs/promises');
const path=require('node:path');
const root=path.resolve(__dirname,'../web');
const server=createServer(async(req,res)=>{
 try{const url=new URL(req.url,'http://localhost');const file=path.resolve(root,'.'+(url.pathname==='/'?'/index.html':url.pathname));if(!file.startsWith(root+path.sep))throw Error('path');res.setHeader('Content-Type',file.endsWith('.js')?'text/javascript':file.endsWith('.json')?'application/json':'text/html');res.end(await fs.readFile(file));}catch{res.statusCode=404;res.end();}
});
(async()=>{
 await new Promise(r=>server.listen(0,'127.0.0.1',r));const base='http://127.0.0.1:'+server.address().port;
 const browser=await chromium.launch();let checks=0;
 try{for(const width of [390,1280]){
  const context=await browser.newContext({viewport:{width,height:850}});const page=await context.newPage();const errors=[];page.on('pageerror',e=>errors.push(e.message));
  await page.goto(base);await page.getByText('Dados fictícios carregados.',{exact:false}).waitFor();
  const fixture=JSON.parse(await fs.readFile(path.join(root,'portfolio.json'),'utf8'));
  assert.equal(await page.locator('#kpis .card').count(),3);
  await page.locator('#tab-holdings').click();await page.locator('#search').fill('absent synthetic name');
  await page.getByText('Nenhuma empresa fictícia encontrada.',{exact:false}).waitFor();
  await page.locator('#reset').click();assert.equal(await page.locator('#search').inputValue(),'');assert.equal(await page.locator('#tab-overview').getAttribute('aria-selected'),'true');checks++;
  const download=page.waitForEvent('download');await page.locator('#export').click();const artifact=await download;const stream=await artifact.createReadStream();const chunks=[];for await(const chunk of stream)chunks.push(chunk);assert.deepEqual(JSON.parse(Buffer.concat(chunks).toString()),fixture);checks++;
  await page.screenshot({path:'/downloads/investor-qa-'+width+'.png'});
  for(const mode of ['offline','corrupt','quota']){
   await page.route('**/portfolio.json',r=>mode==='offline'?r.abort():mode==='quota'?r.fulfill({status:429,body:'{}'}):r.fulfill({contentType:'application/json',body:'{"holdings":"invalid"}'}));
   await page.reload();await page.getByText('Não foi possível carregar a demo.',{exact:false}).waitFor();
   assert(await page.locator('#export').isDisabled());assert(await page.locator('#reset').isDisabled());assert.equal(await page.locator('#kpis .card').count(),0);
   await page.unroute('**/portfolio.json');await page.reload();await page.getByText('Dados fictícios carregados.',{exact:false}).waitFor();assert(!(await page.locator('#export').isDisabled()));checks++;
  }
  await page.route('**/currencies.json',r=>r.abort());await page.reload();await page.locator('#tab-multi').click();await page.getByText('Lista de moedas indisponível.',{exact:false}).waitFor();assert(await page.locator('#multi-apply').isDisabled());await page.unroute('**/currencies.json');await page.reload();await page.locator('#tab-multi').click();await page.locator('#multi-apply:not([disabled])').waitFor();checks++;
  // Data-load failures leave the clear-search button callable; exercise it to
  // expose a known TypeError rather than falsely count the failure UI as safe.
  await page.route('**/portfolio.json',r=>r.abort());await page.reload();await page.getByText('Não foi possível carregar a demo.',{exact:false}).waitFor();await page.locator('#tab-holdings').click();await page.locator('#clear').click();await page.waitForTimeout(50);
  assert(errors.some(e=>/holdings/.test(e)), 'Known defect changed: remove this characterization and assert zero errors');
  console.log(width+': 6 contracts passed; known clear-search-after-load-error defect reproduced');
  await context.close();
 }}finally{await browser.close();server.close();}
 console.log(checks+' browser success/recovery contracts passed. Two known-defect characterizations are NOT passing acceptance criteria.');
})().catch(e=>{console.error(e);server.close();process.exitCode=1;});
