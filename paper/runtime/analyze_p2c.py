import json,sys,statistics as S,collections
R=[json.loads(l) for l in open(sys.argv[1])]
P={ (r["task_id"],r["arm"]):r for r in (json.loads(l) for l in open(sys.argv[2]))}
print(len(R),"rows; is_mock:",set(r["is_mock"] for r in R))
A=collections.defaultdict(dict)
for r in R: A[r["task_id"]][r["arm"]]=r
a1,a2="arm1_basic","arm2_test_guided"
print("task | arm1 final/submitted/ast/end/turns/fe/runs/calls/sec | arm2 ...")
for t,d in A.items():
    row=[]
    for a in (a1,a2):
        r=d[a]; row.append(f"{int(r['resolved_final_state'])}/{int(r['resolved_submitted'])}/{int(bool(r['ast_equal_reference']))}/{r['end_reason']}/{r['turns']}/{r['format_errors']}/{r['test_runs']}/{r['tool_calls']}/{r['wall_seconds']:.0f}s/ft={r['final_tests'].get('failed')}of{r['final_tests'].get('tests')}/edit={r['edits']}/err={r['edit_errors']}")
    print(t[9:],"|"," | ".join(row))
for a in (a1,a2):
    rs=[d[a] for d in A.values()]
    f=lambda k:sum(r[k] for r in rs)
    print(a,"resolved_final",sum(r["resolved_final_state"] for r in rs),"resolved_submitted",sum(r["resolved_submitted"] for r in rs),
      "ast_eq",sum(bool(r["ast_equal_reference"]) for r in rs),"submitted",sum(r["submitted"] for r in rs),"syntax_err",sum(r["syntax_error_final"] for r in rs),
      "fmt_err",f("format_errors"),"unknown_tool",f("unknown_tool_calls"),"test_runs",f("test_runs"),"tool_calls",f("tool_calls"),"edits",f("edits"),"edit_errors",f("edit_errors"),
      "turns",f("turns"),"wall_total",round(f("wall_seconds")),"mean_wall",round(S.mean(r["wall_seconds"] for r in rs),1),"prompt_tok",f("prompt_tokens"),"compl_tok",f("completion_tokens"),
      "ctx_trunc",f("context_truncations"),"end",dict(collections.Counter(r["end_reason"] for r in rs)),"nonzero_diff",sum(r["diff_lines_changed"]>0 for r in rs))
# paired
both=sum(d[a1]["resolved_final_state"] and d[a2]["resolved_final_state"] for d in A.values())
o1=sum(d[a1]["resolved_final_state"] and not d[a2]["resolved_final_state"] for d in A.values())
o2=sum((not d[a1]["resolved_final_state"]) and d[a2]["resolved_final_state"] for d in A.values())
print("paired both",both,"only_arm1",o1,"only_arm2",o2,"neither",12-both-o1-o2)
# pilot vs main
for k,p in P.items():
    m=A[k[0]][k[1]]
    print("pilot-vs-main",k[0][9:],k[1],"pilot",p["resolved_final_state"],"main",m["resolved_final_state"],"turns",p["turns"],m["turns"],"patch_same",p["patch"]==m["patch"])
