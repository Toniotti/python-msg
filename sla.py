months      = int(input("Quantos meses: "))
pct         = int(input("Porcentagem de ganho mensal: "))
starts_with = int(input("Começa com: "))
add_by      = int(input("Adiciona por mes: "))
total       = starts_with
lt          = starts_with

for i in range(months):
        if i != 0:
                total += (total*(pct/100))+add_by
        print("No mes ", (i+1), " o total na conta é: %.3f" %total)
        print("Ganho no mes: %.2f" %((total-lt)-add_by))
        lt = total
    
    
print("O total na conta é: %.3f" %total)
print("O total ganho é %.3f" %(total-(add_by*months)))
