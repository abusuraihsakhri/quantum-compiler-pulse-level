const test=require("node:test"),assert=require("node:assert/strict");
const {evaluate}=require("../web/app.js");
const sample={task_id:"T1",target_identifier:"K1",primary_metric:20,secondary_metric:5,status_descriptor:"NOMINAL",is_critical_flag:false};
test("enterprise nominal",()=>assert.equal(evaluate(sample).overall_urgency,"ROUTINE"));
test("enterprise escalation and 3 alerts",()=>{const result=evaluate({...sample,primary_metric:26,secondary_metric:13,is_critical_flag:true,status_descriptor:"ANOMALY"});assert.equal(result.total_alerts,3);assert.equal(result.critical_alerts_count,1);});
test("pulse secondary cutoff",()=>assert.equal(evaluate({...sample,mode:"pulse",secondary_metric:11}).overall_status,"ELEVATED_RISK_WARNING"));
test("pulse flag escalation",()=>assert.equal(evaluate({...sample,mode:"pulse",is_critical_flag:true}).overall_status,"CRITICAL_INTERVENTION_REQUIRED"));
test("invalid input",()=>{assert.throws(()=>evaluate({...sample,primary_metric:"NaN"}));assert.throws(()=>evaluate({...sample,task_id:" "}));});
test("different protocol flags",()=>{assert.equal(evaluate({...sample,status_descriptor:"FAIL"}).total_alerts,1);assert.equal(evaluate({...sample,mode:"pulse",status_descriptor:"FAIL"}).total_alerts,0);});
