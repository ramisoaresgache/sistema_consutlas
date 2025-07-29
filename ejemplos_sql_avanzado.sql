-- EJEMPLOS DE SQL AVANZADO PARA EL SISTEMA DE CONSULTAS
-- Demostrando tablas temporales y lógica condicional

-- =====================================================
-- 1. EJEMPLO: TABLA TEMPORAL PARA ANÁLISIS DE PLANES
-- =====================================================

-- Crear tabla temporal con resumen de planes
CREATE TEMP TABLE temp_resumen_planes AS
SELECT 
    a.n_plan as plan,
    a.c_estado as estado_codigo,
    COUNT(b.n_cuota_plan) as total_cuotas,
    SUM(b.i_capital) as total_capital,
    SUM(b.i_recargo) as total_recargos,
    SUM(CASE WHEN b.f_pago IS NOT NULL THEN 1 ELSE 0 END) as cuotas_pagadas
FROM ppc_cab a
LEFT JOIN cuotas_ppc b ON a.n_plan = b.n_plan
GROUP BY a.n_plan, a.c_estado;

-- Usar la tabla temporal en consulta final
SELECT 
    plan,
    estado_codigo,
    total_cuotas,
    total_capital,
    total_recargos,
    cuotas_pagadas,
    (total_cuotas - cuotas_pagadas) as cuotas_pendientes,
    CASE 
        WHEN cuotas_pagadas = total_cuotas THEN 'COMPLETO'
        WHEN cuotas_pagadas > 0 THEN 'PARCIAL'
        ELSE 'SIN PAGOS'
    END as estado_pago
FROM temp_resumen_planes
WHERE plan = 12345;

-- =====================================================
-- 2. EJEMPLO: CTE (Common Table Expression)
-- =====================================================

-- Alternativa moderna a tablas temporales
WITH resumen_cuentas AS (
    SELECT 
        c_cuenta,
        c_sistema,
        COUNT(*) as total_transacciones,
        SUM(i_capital) as total_capital
    FROM transacciones 
    WHERE c_actual = 'S'
    GROUP BY c_cuenta, c_sistema
),
cuentas_activas AS (
    SELECT * 
    FROM resumen_cuentas 
    WHERE total_capital > 1000
)
SELECT 
    c_cuenta,
    c_sistema,
    total_transacciones,
    total_capital,
    CASE 
        WHEN total_capital > 50000 THEN 'ALTO'
        WHEN total_capital > 10000 THEN 'MEDIO'
        ELSE 'BAJO'
    END as categoria_deuda
FROM cuentas_activas;

-- =====================================================
-- 3. EJEMPLOS DE LÓGICA CONDICIONAL (CASE WHEN)
-- =====================================================

-- Ejemplo 1: Estado de deuda categorizado
SELECT 
    c_cuenta,
    i_capital,
    f_vencimiento,
    CASE 
        WHEN f_vencimiento < TODAY THEN 'VENCIDA'
        WHEN f_vencimiento = TODAY THEN 'VENCE HOY'
        WHEN f_vencimiento <= TODAY + 30 THEN 'VENCE PRONTO'
        ELSE 'AL DIA'
    END as estado_vencimiento,
    CASE 
        WHEN i_capital > 100000 THEN 'DEUDA ALTA'
        WHEN i_capital > 10000 THEN 'DEUDA MEDIA'
        WHEN i_capital > 0 THEN 'DEUDA BAJA'
        ELSE 'SIN DEUDA'
    END as categoria_deuda
FROM cta_cte
WHERE c_cuenta = '12345';

-- Ejemplo 2: Análisis de declaraciones juradas
SELECT 
    n_cuit,
    c_cuenta,
    n_ano,
    c_baja,
    CASE 
        WHEN c_baja = 1 THEN 'DADA DE BAJA'
        WHEN c_baja = 0 AND n_ano = YEAR(TODAY) THEN 'ACTIVA CORRIENTE'
        WHEN c_baja = 0 AND n_ano < YEAR(TODAY) THEN 'ACTIVA ATRASADA'
        ELSE 'ESTADO INDEFINIDO'
    END as estado_detallado,
    CASE 
        WHEN n_ano = YEAR(TODAY) THEN 'PERIODO ACTUAL'
        WHEN n_ano = YEAR(TODAY) - 1 THEN 'PERIODO ANTERIOR'
        ELSE 'PERIODO HISTORICO'
    END as categoria_periodo
FROM ddjj_sh_cab
WHERE n_cuit = 20123456789;

-- =====================================================
-- 4. EJEMPLO: SUBCONSULTAS CON LÓGICA CONDICIONAL
-- =====================================================

-- Consulta de planes con estado calculado dinámicamente
SELECT 
    p.n_plan,
    p.c_estado,
    p.n_cant_cuotas,
    (SELECT COUNT(*) FROM cuotas_ppc c WHERE c.n_plan = p.n_plan AND c.f_pago IS NOT NULL) as cuotas_pagadas,
    CASE 
        WHEN p.c_estado = 'C' THEN 'CANCELADO'
        WHEN (SELECT COUNT(*) FROM cuotas_ppc c WHERE c.n_plan = p.n_plan AND c.f_pago IS NOT NULL) = p.n_cant_cuotas 
             THEN 'TOTALMENTE PAGADO'
        WHEN (SELECT COUNT(*) FROM cuotas_ppc c WHERE c.n_plan = p.n_plan AND c.f_pago IS NOT NULL) > 0 
             THEN 'PARCIALMENTE PAGADO'
        ELSE 'SIN PAGOS'
    END as estado_real
FROM ppc_cab p
WHERE p.n_plan = 12345;

-- =====================================================
-- 5. EJEMPLO: FUNCIÓN WINDOW CON CASE
-- =====================================================

-- Ranking de deudores con categorización
SELECT 
    c_cuenta,
    SUM(i_capital) as total_deuda,
    ROW_NUMBER() OVER (ORDER BY SUM(i_capital) DESC) as ranking,
    CASE 
        WHEN ROW_NUMBER() OVER (ORDER BY SUM(i_capital) DESC) <= 10 THEN 'TOP 10'
        WHEN ROW_NUMBER() OVER (ORDER BY SUM(i_capital) DESC) <= 50 THEN 'TOP 50'
        ELSE 'OTROS'
    END as categoria_ranking
FROM cta_cte
WHERE c_estado_deuda = 'D'
GROUP BY c_cuenta
ORDER BY total_deuda DESC;

-- =====================================================
-- 6. EJEMPLO COMPLEJO: MÚLTIPLES TABLAS TEMPORALES
-- =====================================================

-- Paso 1: Crear tabla temporal de resumen por cuenta
CREATE TEMP TABLE temp_resumen_cuenta AS
SELECT 
    c_cuenta,
    SUM(i_capital) as total_capital,
    SUM(i_recargo) as total_recargo,
    COUNT(*) as total_registros
FROM cta_cte
WHERE c_estado_deuda = 'D'
GROUP BY c_cuenta;

-- Paso 2: Crear tabla temporal de clasificación
CREATE TEMP TABLE temp_clasificacion AS
SELECT 
    c_cuenta,
    total_capital,
    total_recargo,
    total_registros,
    CASE 
        WHEN total_capital > 500000 THEN 'CRITICO'
        WHEN total_capital > 100000 THEN 'ALTO'
        WHEN total_capital > 10000 THEN 'MEDIO'
        ELSE 'BAJO'
    END as nivel_riesgo
FROM temp_resumen_cuenta;

-- Paso 3: Consulta final usando ambas tablas temporales
SELECT 
    tc.c_cuenta,
    tc.total_capital,
    tc.total_recargo,
    tc.nivel_riesgo,
    CASE 
        WHEN tc.nivel_riesgo = 'CRITICO' THEN 'ACCION INMEDIATA'
        WHEN tc.nivel_riesgo = 'ALTO' THEN 'SEGUIMIENTO CERCANO'
        WHEN tc.nivel_riesgo = 'MEDIO' THEN 'MONITOREO REGULAR'
        ELSE 'REVISION PERIODICA'
    END as accion_recomendada
FROM temp_clasificacion tc
ORDER BY tc.total_capital DESC;
