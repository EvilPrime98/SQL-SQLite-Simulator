import re

secuence_int = 0

def integer_secuence():
    global secuence_int  
    secuence_int = secuence_int + 1
    return secuence_int

def replace_nextval(match):
    return '(' + str(integer_secuence()) + ','

def convert_sqlite_syntax(sql):
    sql = re.sub(r'\b(\w+)\.\s*NEXTVAL\b', r'\1.NEXTVAL', sql, flags=re.IGNORECASE)
    sql = re.sub(r'\bVARCHAR2\b', 'TEXT', sql, flags=re.IGNORECASE)
    sql = re.sub(r'\bNUMBER\b', 'NUMERIC', sql, flags=re.IGNORECASE)
    sql = re.sub(r'\bDATE\b', 'TEXT', sql, flags=re.IGNORECASE)
    sql = re.sub(r'\bTIMESTAMP\b', 'TEXT', sql, flags=re.IGNORECASE)
    sql = re.sub(r';*?\bCREATE SEQUENCE\b.*?;', '', sql, flags=re.IGNORECASE | re.DOTALL)
    sql = re.sub(r';*?\bCOMMIT\b.*?;', '', sql, flags=re.IGNORECASE | re.DOTALL)
    sql = re.sub(r'\([^)]+\.NEXTVAL,', replace_nextval, sql, flags=re.IGNORECASE)
    sql = re.sub(r'\n\s*\n', '\n', sql)
    sql = sql.strip()
    return sql

def oracle_to_sqlite(input_file, output_file):
    with open(input_file, 'r') as f:
        oracle_sql = f.read()

    sqlite_sql = convert_sqlite_syntax(oracle_sql)

    with open(output_file, 'w') as f:
        f.write(sqlite_sql)

    print(f'Archivo convertido exitosamente: {output_file}')

if __name__ == "__main__":
    oracle_file = 'TiendaInf.sql'
    sqlite_file = 'TiendaInf_SQL_LITE.sql'
    oracle_to_sqlite(oracle_file, sqlite_file)