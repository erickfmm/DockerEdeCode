from inspect import getframeinfo, currentframe
from multiprocessing import current_process

import ede.ede.check_utils as check_utils
from ede.ede._logger import logger


def fn3E8(conn, return_dict):
    """
    INTEGRIDAD DE DATOS
    
    Verifica que la rama está dentro de la lista permitida
    Args:
        conn ([sqlalchemy.engine.Connection]): [
          Objeto que establece la conexión con la base de datos.
          Creado previamente a través de la función execute(self)
          ]
    Returns:
        [Boolean]: [
          Retorna True/False y "S/Datos" a través de logger, solo si puede:
            - No hay ramas registradas
          Retorna True y “Aprobado” a través de logger, solo si se puede: 
            - Todas las ramas están dentro de la lista permitida
          En todo otro caso, retorna False y "Rechazado" a través de logger.
          ]
    """
    _r = False
    rows = []
    try:
        rows = conn.execute(
            "SELECT RBD,nombreEstablecimiento,modalidad,jornada,nivel,rama,sector,especialidad,tipoCurso,codigoEnseñanza,grado,letraCurso FROM jerarquiasList;").fetchall()
    except Exception as e:
        logger.info(f"Resultado: {rows} -> {str(e)}")

    try:
        ramaList = check_utils.convertirArray2DToList(
            list(set([m[5] for m in rows if m[5] is not None])))
        if(len(ramaList) > 0):
            _err = set([e for e in ramaList if not check_utils.validaRama(e)])
            _r = False if len(_err) > 0 else True
            _t = f"VERIFICA QUE LA RAMA ESTA DENTRO DE LA LISTA PERMITIDA: {_r}. {_err}"
            logger.info(_t) if _r else logger.error(_t)
            logger.info(f"Aprobado") if _r else logger.error(f"Rechazado")
        else:
            logger.info("S/Datos")
    except Exception as e:
        logger.error(f"No se pudo ejecutar la verificación: {str(e)}")
        logger.error(f"Rechazado")
    finally:
        return_dict[getframeinfo(currentframe()).function] = _r
        logger.info(f"{current_process().name} finalizando...")
        return _r
