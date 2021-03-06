from data_collection.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):

    council_id = "E07000147"
    addresses_name = "parl.2019-12-12/Version 1/merged.CSV"
    stations_name = "parl.2019-12-12/Version 1/merged.CSV"
    elections = ["parl.2019-12-12"]
    allow_station_point_from_postcode = False

    def address_record_to_dict(self, record):
        rec = super().address_record_to_dict(record)
        uprn = record.property_urn.strip().lstrip("0")

        if uprn in [
            "10023457014",
            "100091325096",
            "10034807115",
        ]:
            return None

        if record.addressline6 == "NR12 0RX":
            return None

        return rec
