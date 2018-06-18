from ..utils.json import JSONObject
from ..backend import *

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
    with LeanDataset(fibers, 'result') as lgd:
        if "score" in res:
            if "raw" in res.score:
                lgd.data['raw'] = _score_parser(res.score.raw)
            if "min" in res.score:
                lgd.data['min'] = _score_parser(res.score.min)
            if "max" in res.score:
                lgd.data['max'] = _score_parser(res.score.max)
            if "scaled" in res.score:
                lgd.data['scaled'] = _score_parser(res.score.scaled)
        if "success" in res:
            lgd.data['success'] = res.success
        if "response" in res:
            lgd.data['response'] = res.response
