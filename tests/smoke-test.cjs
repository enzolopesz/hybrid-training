/* Testes de lógica sem navegador, usando Node.js: node tests/smoke-test.cjs */
const fs = require('node:fs');
const path = require('node:path');
const vm = require('node:vm');
const assert = require('node:assert/strict');
const source = fs.readFileSync(path.join(__dirname, '../app.js'),'utf8');
const memory = new Map();
const elements = new Map();
function el(id){if(!elements.has(id))elements.set(id,{
  id, innerHTML:'', textContent:'', value:'', addEventListener(){}, classList:{add(){},remove(){},toggle(){}},
});return elements.get(id)}
const sandbox={
 localStorage:{getItem:k=>memory.get(k)||null, setItem:(k,v)=>memory.set(k,String(v))},
 document:{getElementById:el,querySelectorAll:()=>[],addEventListener(){}},
 window:{scrollTo(){}}, navigator:{},location:{protocol:'file:',hostname:'localhost'},
 Date,Math,Number,String,Array,Object,JSON,Intl,RegExp,console,clearTimeout,setTimeout:()=>0,setInterval:()=>0,
 FileReader:class{readAsText(file){this.result=file.content;this.onload()}},
 confirm:()=>true,alert:msg=>{throw Error(String(msg))},
};
vm.createContext(sandbox);
vm.runInContext(source,sandbox,{filename:'app.js'});
const read=(code)=>vm.runInContext(code,sandbox);
const exec=(code)=>vm.runInContext(code,sandbox);
assert.equal(read('state.version'),2);
assert.equal(read('state.plans.A.exercises.length'),7);
assert.equal(read('state.plans.B.exercises[1].id'),'extensao_45');
assert.equal(read('effectiveType("2026-10-12")'),'EASY');
assert.equal(read('effectiveType("2026-10-13")'),'REST');
assert.equal(read('effectiveType("2026-10-20")'),'EASY');
assert.equal(read('effectiveType("2026-11-18")'),'EASY');
assert.equal(read('state.events["2026-11-15"].kind'),'race');
assert.equal(read('renderProgress().includes("Corrida semanal")'),true);
// Registra pesos, repetições e confirmação de série, com cronômetro iniciado.
exec('selected="2026-10-19";selectedType=null');
exec('adjustSet("supino_reto",0,"kg",50)');
exec('adjustSet("supino_reto",0,"reps",8)');
exec('markSet("supino_reto",0)');
assert.equal(read('state.sessions["2026-10-19|A"].exercises.supino_reto[0].kg'),'50');
assert.equal(read('state.sessions["2026-10-19|A"].exercises.supino_reto[0].done'),true);
assert.equal(read('state.timer.running'),true);
assert.equal(read('JSON.parse(localStorage.getItem(STORE)).sessions["2026-10-19|A"].exercises.supino_reto[0].reps'),'8');
// A edição da ficha não altera exercícios dos treinos já registrados.
exec('state.plans.A.exercises[0].name="Supino alterado"');
assert.equal(read('exFor("A",state.sessions["2026-10-19|A"])[0].name'),'Supino reto com barra');
// Trocar tipo do treino de uma data não altera as outras datas da semana.
exec('selectedType="C"');
assert.equal(read('typeFor("2026-10-19")'),'C');
assert.equal(read('typeFor("2026-10-21")'),'B');
// Personalização de um dia específico fica gravada para reabrir depois.
exec('selected="2026-10-21";selectedType=null');
exec('handleInput({dataset:{action:"switch-type"},value:"EASY"})');
assert.equal(read('state.overrides["2026-10-21"]'),'EASY');
assert.equal(read('effectiveType("2026-10-21")'),'EASY');
assert.equal(read('effectiveType("2026-10-22")'),'C');
// Importação de calendário .ics sem conexão com Runna.
const ics='BEGIN:VCALENDAR\nBEGIN:VEVENT\nDTSTART;VALUE=DATE:20261208\nSUMMARY:Runna Corrida leve 7 km\nDESCRIPTION:Corrida teste\nEND:VEVENT\nEND:VCALENDAR';
sandbox.icsFixture={content:ics};
exec('importICS(icsFixture)');
assert.equal(read('state.events["2026-12-08"].source'),'ics');
assert.equal(read('state.events["2026-12-08"].distance'),'7');
// Migração de v1 e integridade do conjunto de registros.
const legacy={version:1,sessions:{'2026-10-19|A':{date:'2026-10-19',type:'A',exercises:{supino_reto:[{kg:'45',reps:'8',done:true}]},run:{},notes:'teste'}}};
memory.set('hybridTrainingPersonalV1',JSON.stringify(legacy));
const migrated=read('normalized(JSON.parse(localStorage.getItem("hybridTrainingPersonalV1")))');
assert.equal(migrated.version,2);
assert.equal(migrated.sessions['2026-10-19|A'].exercises.supino_reto[0].kg,'45');
assert.equal(migrated.sessions['2026-10-19|A'].snapshotExercises[0].name,'Supino reto com barra');
assert.equal(!!memory.get('hybridTrainingPersonalV1'),true);
// Mudanças no estado não devem introduzir um erro ao renderizar todas as telas.
exec('selectedType=null;selected="2026-10-19"');
for(const t of ['home','training','calendar','progress','settings']){
 exec(`tab=${JSON.stringify(t)};render()`);
 assert.ok(el('app').innerHTML.length>100,t+' vazia');
}
console.log('✅ 26 verificações de funcionamento e compatibilidade passaram.');
