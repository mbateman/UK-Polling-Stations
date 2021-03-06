import requests
from addressbase.models import Address


def get_stat_from_nomis(dataset, measure, gss_code):
    url = "http://www.nomisweb.co.uk/api/v01/dataset/{dataset}.data.json?date=latest&geography={gss_code}&rural_urban=0&cell=0&measures={measures}".format(
        dataset=dataset, gss_code=gss_code, measures=measure
    )
    r = requests.get(url)
    if r.status_code != 200:
        return 0
    data = r.json()
    if "error" in data:
        return 0
    return data["obs"][0]["obs_value"]["value"]


class Dwellings:
    def from_census(self, gss_code):
        return get_stat_from_nomis("NM_618_1", "20100", gss_code)

    def from_addressbase(self, polygon):
        return Address.objects.filter(location__within=polygon).count()
