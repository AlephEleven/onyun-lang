from ds import *
from readkw import *
import math

def expr(val):
    match val:
        case float(v) | int(v):
            return ast.expr_cls("Num", v, f"Num {v}")
        case str(v):
            return ast.expr_cls("Var", v, f"Var {v}")
        case bool(v):
            return ast.expr_cls("Bool", v, f"Bool {v}")
        case None:
            return ast.expr_cls("Unit", None, "Unit")

def string_of_expr(val):
    match val.id:
        case "Ok":
            return f"Ok ({string_of_expr(val.vals)})"
        case "Num" | "Var" | "Bool":
            return f"{val.id} {val.vals}"
        case "Unit":
            return val.id

def return_expr(val):
    return return_exp(expr(val))

g_env = {}

def eval_expr(exp):
    global g_env
    match exp.id:
        case "Num":
            (n) = exp
            return return_exp(n)
        case "Var":
            (n) = exp
            return eval_expr(apply_env(n.vals, g_env))
        case "Bool":
            (n) = exp
            return return_exp(n)
        case "EAdd":
            (n) = valid_args(exp, 2)
            v1 = num_of_numVal(eval_expr(n[0]))
            v2 = num_of_numVal(eval_expr(n[1]))
            return return_expr(v1+v2)
        case "ESub":
            (n) = valid_args(exp, 2)
            v1 = num_of_numVal(eval_expr(n[0]))
            v2 = num_of_numVal(eval_expr(n[1]))
            return return_expr(v1-v2)
        case "EMul":
            (n) = valid_args(exp, 2)
            v1 = num_of_numVal(eval_expr(n[0]))
            v2 = num_of_numVal(eval_expr(n[1]))
            return return_expr(v1*v2)
        case "EDiv":
            (n) = valid_args(exp, 2)
            v1 = num_of_numVal(eval_expr(n[0]))
            v2 = num_of_numVal(eval_expr(n[1]))
            if(v2==0):
                return error("Div: Division by zero!")
            return return_expr(v1/v2)
        case "EMod":
            (n) = valid_args(exp, 2)
            v1 = num_of_numVal(eval_expr(n[0]))
            v2 = num_of_numVal(eval_expr(n[1]))
            return return_expr(v1%v2)       
        case "EAbs":
            (n) = valid_args(exp, 1)
            v = num_of_numVal(eval_expr(n[0]))
            return return_expr(abs(v))
        case "EMax":
            (n) = valid_args(exp)
            vs = [num_of_numVal(eval_expr(ni)) for ni in n]
            if(len(vs)==0):
                return error("Max: function requires 1> arguments!")
            return return_expr(max(vs))
        case "EMin":
            (n) = valid_args(exp)
            vs = [num_of_numVal(eval_expr(ni)) for ni in n]
            if(len(vs)==0):
                return error("Min: function requires 1> arguments!")
            return return_expr(min(vs))
        case "EInt":
            (n) = valid_args(exp, 1)
            v = num_of_numVal(eval_expr(n[0]))
            return return_expr(int(v))
        case "EExp":
            (n) = valid_args(exp, 1)
            v = num_of_numVal(eval_expr(n[0]))
            return return_expr(math.exp(v))
        case "EIszero":
            (n) = valid_args(exp, 1)
            v = num_of_numVal(eval_expr(n[0]))
            return return_expr(v==0)
        case "ESet":
            (n) = valid_args(exp, 2)
            id = n[0].vals
            defin = eval_expr(n[1]).vals
            g_env = extend_env(id, defin, g_env)
            return return_expr(None)
        case "ECell":
            (n) = valid_args(exp)
            vs = [eval_expr(n1) for n1 in n[:-1]]+[n[-1]]
            return eval_expr(vs[-1])
        case "EPrivcell":
            (n) = valid_args(exp)
            temp = g_env
            g_env = {}
            
            vs = [eval_expr(n1) for n1 in n[:-1]]+[n[-1]]
            res = eval_expr(vs[-1])
            
            g_env = temp
            return res

        case any:
            return error(f"Interp Error: Not Implemented ({any})")

def interp(line):
    return eval_expr(ast.parse_AST(line))

def interpS(line):
    return "Onyun: "+string_of_expr(interp(line))

