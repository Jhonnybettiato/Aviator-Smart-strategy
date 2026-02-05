import os

def calcular_apuesta(saldo_inicial, perdida_acumulada, meta_sesion):
    # Estrategia de recuperación conservadora
    if perdida_acumulada == 0:
        return round(saldo_inicial * 0.02, 2)  # Apuesta base: 2% del saldo
    else:
        # Calcula cuánto apostar para recuperar la pérdida en un cobro de 1.50x
        recuperacion = (perdida_acumulada * 2) 
        return round(min(recuperacion, saldo_inicial * 0.1), 2) # Máximo 10% para no quebrar

def analizar_vuelos(historial):
    if not historial: return "Esperando datos...", 1.20
    recientes = historial[-3:]
    promedio = sum(recientes) / len(recientes)
    
    if all(x < 1.50 for x in recientes):
        return "⚠️ ALERTA: Racha fría. NO APOSTAR.", 0
    if recientes[-1] > 10.0:
        return "📉 AVISO: Rosa alto detectado. Espera 2 rondas.", 0
    if promedio > 2.0:
        return "✅ SEÑAL: Racha estable.", 1.50
    return "🔍 ESTADO: Mercado lento.", 1.20

def main():
    os.system('cls' if os.name == 'nt' else 'clear')
    print("=== 🦅 AVIATOR ESTRATEGA v1.5 ===")
    saldo = float(input("¿Cuál es tu saldo actual en Gs/USD?: "))
    meta = saldo * 1.2  # Meta: Ganar un 20%
    historial = []
    perdida_total = 0
    
    while saldo < meta and saldo > 0:
        os.system('cls' if os.name == 'nt' else 'clear')
        print(f"💰 Saldo: {saldo:.2f} | 🎯 Meta: {meta:.2f} | 📉 Deuda: {perdida_total:.2f}")
        print(f"Últimos resultados: {historial[-5:]}")
        
        msg, sugerencia_auto = analizar_vuelos(historial)
        apuesta_sugerida = calcular_apuesta(saldo, perdida_total, meta)
        
        print(f"\n💡 ESTRATEGIA: {msg}")
        if sugerencia_auto > 0:
            print(f"👉 APUESTA RECOMENDADA: {apuesta_sugerida:.2f}")
            print(f"👉 CONFIGURA AUTO CASHOUT EN: {sugerencia_auto}x")
        else:
            print("👉 ACCIÓN: Mantente fuera de esta ronda.")

        valor = input("\nResultado del avión (o 'p' si perdiste tu apuesta): ").strip().lower()
        
        if valor == 'p':
            perdida_total += apuesta_sugerida
            saldo -= apuesta_sugerida
        elif valor != '':
            try:
                num = float(valor)
                historial.append(num)
                if sugerencia_auto > 0 and num >= sugerencia_auto:
                    # Si ganamos, recuperamos la deuda y sumamos ganancia
                    saldo += (apuesta_sugerida * sugerencia_auto) - apuesta_sugerida
                    perdida_total = 0
                    print("¡GANASTE! 🎉")
                elif sugerencia_auto > 0 and num < sugerencia_auto:
                    # Si el script dijo apuesta y el avión se fue antes
                    perdida_total += apuesta_sugerida
                    saldo -= apuesta_sugerida
                    print("Perdiste esta ronda. Calculando recuperación...")
            except: pass

    if saldo >= meta:
        print("\n¡FELICIDADES! Alcanzaste tu meta. Retira y cierra el juego. 🥂")
    else:
        print("\nSaldo agotado. Revisa tu estrategia. ❌")

if __name__ == "__main__":
    main()
