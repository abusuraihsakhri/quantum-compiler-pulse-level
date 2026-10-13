"use strict";
(function(root) {
  function evaluate(data) {
    const pulse = data.mode === "pulse";
    if (data.primary_metric === "" || data.secondary_metric === "") throw Error("Both numeric metrics are required.");
    const p = Number(data.primary_metric), s = Number(data.secondary_metric);
    if (!Number.isFinite(p) || !Number.isFinite(s)) throw Error("Metrics must be finite numbers.");
    const task_id = String(data.task_id || "").trim();
    const target_identifier = String(data.target_identifier || "").trim();
    if (!task_id || !target_identifier) throw Error("Task ID and target ID are required.");
    if (task_id.length > 200 || target_identifier.length > 200) throw Error("Identifiers exceed 200 characters.");
    const descriptor = String(data.status_descriptor || "NOMINAL");
    const critical = data.is_critical_flag === true;
    const alerts = [];
    function add(name,urgency,summary,details) {
      if (pulse) alerts.push({origin_agent:name,status:urgency,summary,technical_details:details});
      else alerts.push({origin_worker:name,urgency,summary,technical_details:details});
    }
    if (pulse) {
      if (p>25) add("DRAGPulseShaperAgent","ELEVATED_RISK_WARNING","Primary threshold exceeded","Primary metric exceeds 25.");
      if (s>10 || critical) add("RabiOscillationAnalyzerAgent",critical?"CRITICAL_INTERVENTION_REQUIRED":"ELEVATED_RISK_WARNING","Secondary threshold or critical flag","Secondary metric exceeds 10 or critical flag is set.");
      if (/VIOLATION|DISCORDANT|ANOMALY|MUTANT|LEAK/i.test(descriptor)) add("StateLeakageAuditorAgent","ELEVATED_RISK_WARNING","Descriptor flag","Status descriptor matches a flagged term.");
      const critical_count = alerts.filter(x=>x.status==="CRITICAL_INTERVENTION_REQUIRED").length;
      return {mode:"pulse",task_id,target_identifier,overall_status:critical_count?"CRITICAL_INTERVENTION_REQUIRED":alerts.length?"ELEVATED_RISK_WARNING":"NOMINAL_OPTIMAL",total_alerts:alerts.length,critical_count,warning_count:alerts.length-critical_count,alerts};
    }
    if (p>25) add("InvariantQCWorker","ELEVATED_RISK","Primary threshold exceeded","Primary metric exceeds 25.");
    if (s>12 || critical) add("SafetyEscalationWorker",critical?"CRITICAL_STAT_PANIC":"ELEVATED_RISK","Secondary threshold or critical flag","Secondary metric exceeds 12 or critical flag is set.");
    if (/DISCORDANT|ANOMALY|MUTANT|VIOLATION|FAIL|REJECT/i.test(descriptor)) add("ProtocolConformanceWorker","ELEVATED_RISK","Descriptor flag","Status descriptor matches a flagged term.");
    const critical_alerts_count = alerts.filter(x=>x.urgency==="CRITICAL_STAT_PANIC").length;
    return {mode:"enterprise",task_id,target_identifier,overall_urgency:critical_alerts_count?"CRITICAL_STAT_PANIC":alerts.length?"ELEVATED_RISK":"ROUTINE",integrity_status:critical_alerts_count?"RECALIBRATION_REQUIRED":alerts.length?"DISCORDANT_ANOMALY":"VALIDATED_OPTIMAL",total_alerts:alerts.length,critical_alerts_count,alerts};
  }
  if (typeof module !== "undefined" && module.exports) module.exports = {evaluate};
  if (typeof document === "undefined") return;
  document.addEventListener("DOMContentLoaded", function() {
    const form=document.getElementById("form");
    const output=document.getElementById("output");
    const status=document.getElementById("status");
    const count=document.getElementById("count");
    const save=document.getElementById("save");
    const mode=document.getElementById("mode");
    const note=document.getElementById("note");
    let n=0,last=null;
    mode.addEventListener("change",function() {
      note.textContent=mode.value==="pulse"?"Pulse demonstration: primary > 25, secondary > 10, or descriptor/critical flag.":"Enterprise demonstration: primary > 25, secondary > 12, or descriptor/critical flag.";
    });
    form.addEventListener("submit",function(event) {
      event.preventDefault();
      const data={mode:mode.value,is_critical_flag:document.getElementById("critical").checked};
      for(const key of ["task_id","target_identifier","primary_metric","secondary_metric","status_descriptor"]) data[key]=document.getElementById(key).value;
      try {
        last=evaluate(data);
        status.textContent=last.overall_status||last.overall_urgency;
        output.textContent=JSON.stringify(last,null,2);
        count.textContent=String(++n);
        save.disabled=false;
      } catch(err) {
        last=null;
        save.disabled=true;
        status.textContent="Input error";
        output.textContent=err.message;
      }
    });
    save.addEventListener("click",function() {
      if(!last)return;
      const url=URL.createObjectURL(new Blob([JSON.stringify(last,null,2)+"\n"],{type:"application/json"}));
      const a=document.createElement("a");
      a.href=url;a.download="evaluation.json";a.click();
      setTimeout(function(){URL.revokeObjectURL(url);},1000);
    });
  });
})(typeof globalThis!=="undefined"?globalThis:this);
