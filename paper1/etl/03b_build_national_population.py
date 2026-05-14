"""
03b_build_national_population.py — ETL: Denominador poblacional nacional Base 2024
Proyecto v4.0

Lee proyecciones INE base 2024 (nivel país), y calcula la población nacional interpolada mensualmente.
"""

import pandas as pd
import numpy as np
from pathlib import Path

def build_national_population():
    print("  Reading INE base 2024 national projections...")
    file_path = Path("data/Poblacion_nacional_base_2024/estimaciones-y-proyecciones-de-población-1992-2070_base-2024_base-de-datos.xlsx")
    df = pd.read_excel(file_path)
    
    # Parse FECHA and keep only mid-year estimates (June)
    df['date'] = pd.to_datetime(df['FECHA'], dayfirst=True)
    df = df[df['date'].dt.month == 6].copy()
    df['year'] = df['date'].dt.year
    
    # Group by year
    pop_annual = df.groupby('year')['POBLACION'].sum().reset_index()
    pop_annual = pop_annual[pop_annual['year'].between(2013, 2025)].copy()
    
    print("  Interpolating monthly population...")
    rows = []
    
    for _, row in pop_annual.iterrows():
        year = int(row["year"])
        pop_this_year = row["POBLACION"]
        
        # Buscar pop del año siguiente
        next_row = pop_annual[pop_annual["year"] == year + 1]
        if len(next_row) > 0:
            pop_next = next_row["POBLACION"].values[0]
        else:
            # Extrapolar con pendiente del año anterior
            prev_row = pop_annual[pop_annual["year"] == year - 1]
            if len(prev_row) > 0:
                pop_next = pop_this_year + (pop_this_year - prev_row["POBLACION"].values[0])
            else:
                pop_next = pop_this_year
        
        for month in range(1, 13):
            pop_monthly = pop_this_year + (month - 6.5) / 12 * (pop_next - pop_this_year)
            rows.append({
                "year": year,
                "month": month,
                "pop_nacional_base2024": int(round(pop_monthly))
            })
            
    return pd.DataFrame(rows)

def main():
    output_path = Path("paper1/output/data/poblacion_nacional_mensual_base2024.csv")
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    pop_monthly = build_national_population()
    
    print(f"\nDataframe shape: {pop_monthly.shape}")
    print(f"\nSample (2024):")
    print(pop_monthly[pop_monthly["year"] == 2024].to_string(index=False))
    
    print(f"\nSaving to {output_path}...")
    pop_monthly.to_csv(output_path, index=False)
    print("Done.")

if __name__ == "__main__":
    main()
