/*
 * テンプレート例(jinja2)
 */
.file "{{func_name}}.S"
.text
    .align  2
    .global {{func_name}}
{{func_name}}:
    stmfd sp!, {r4-r7, r9, lr}

    {{op1}}, r0, r0, r1
    {{op2}}, r0, r0, r1
    {{op3}}, r0, r0, r1

    ldmfd sp!, {r4-r7, r9, pc}
