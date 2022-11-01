grammar pseudo;
options {
  language = Python3;
}
prog: (block | record | subroutine)* ;
block:  repeat_until | while_loop |for_loop_step | for_loop| condition_sequence | stat;

repeat_until: 'REPEAT' block* 'UNTIL' expr;
while_loop: 'WHILE' expr block* 'ENDWHILE';
for_loop_step: 'FOR' IDENTIFIER '<-' expr 'TO' expr   ('STEP' step = expr)? block* 'ENDFOR';
for_loop: 'FOR' IDENTIFIER 'IN' expr (block*) 'ENDFOR';
condition_sequence: if_block (else_if_block)* else_block? 'ENDIF';
if_block: 'IF' expr 'THEN' block* ;
record: 'RECORD'  IDENTIFIER (field)* 'ENDRECORD';
field: IDENTIFIER ':'   IDENTIFIER;
else_if_block: 'ELSE IF' expr 'THEN' block*;
else_block: 'ELSE' block*;
arg : IDENTIFIER;
subroutine: 'SUBROUTINE' IDENTIFIER '(' (arg (',' arg)*)? ')' (block*) 'ENDSUBROUTINE';
stat: variable_assignment | output | return_stat | reveal_type | expr  ;
reveal_type: 'reveal_type' expr;

return_stat: 'RETURN' expr;
function_call: IDENTIFIER '(' (expr (',' expr)*)? ')';
output: 'OUTPUT' (expr (',' expr)*)? ;
COMMENT : '#' ~('\r'|'\n')* -> skip ;
variable_assignment: ((CONSTANT? IDENTIFIER) | expr) '<-' expr ;
expr: op=  ('NOT' | '-') expr  #unary_expr
    | expr op= ('MOD' | 'DIV' | '*' | '/') expr #binary_expr
    | expr op = ('+' | '-') expr #binary_expr
    | expr op = ('<' | '>'| '=' | '≠' | '≤' | '≥') expr #binary_expr
    | expr op = ('AND' | 'OR')  expr #binary_expr
    | expr '[' expr ']' #index_expr
    | '(' expr ')' #parenthesis_expr
    | '[' expr? (',' expr)* ']' #array_expr
    | function_call #function_call_expr
    | expr '.' IDENTIFIER #field_access
    | 'USERINPUT' #user_input
    | INT #int
    | FLOAT #real
    | BOOL #bool
    | STRING #string
    | IDENTIFIER #variable
    ;
WS : (' '|'\t'|'\r'|'\n')+ -> skip ;
BOOL: 'True' | 'False' ;
STRING: ('"' .*? '"') | ('\'' .*? '\'') ;

CONSTANT: 'CONSTANT';
IDENTIFIER: LETTER  (LETTER | '_' | INT)* ;
/* Float Literal*/
FLOAT:  (INT '.' INT) ;
/*Int literal */
INT: DIGIT+ ;
/* Digit Literal */
DIGIT: [0-9] ;
/* Letter */
LETTER : [a-zA-Z];

