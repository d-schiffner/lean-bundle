import numpy as np
from utils.json import JSONObject

def _score_parser(stmt):
    if isinstance(stmt, JSONObject):
        if "$numberLong" in stmt:
            return int(stmt["$numberLong"])
        return str(stmt)
    else:
        return stmt

def parse(fibers, statement):
    if not 'result' in statement:
        return
    res = statement.result
    data = []
    if "score" in res:
        if "raw" in res.score:
            data.append(_score_parser(res.score.raw))
        if "min" in res.score:
            data.append(_score_parser(res.score.min))
        if "max" in res.score:
            data.append(_score_parser(res.score.max))
        if "scaled" in res.score:
            data.append(_score_parser(res.score.scaled))
    result_dset = fibers.create_dataset("result", data=data)
    if "success" in res:
        result_dset.attrs["success"] = res.success
    if "response" in res:
        result_dset.attrs["response"] = np.string_(res.response.encode())
