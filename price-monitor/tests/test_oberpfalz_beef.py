import json

from price_monitor.scrapers.oberpfalz_beef import OberpfalzBeefLammScraper


FIXTURE_HTML = """
<html>
<head>
<script id="wbmTagMangerDataLayer" type="text/javascript">
    window.dataLayer.push({ ecommerce: null });
    let onEventDataLayer = JSON.parse('[{"event":"view_item_list","ecommerce":{"item_list_name":"Category: ","items":[{"price":39.71,"index":0,"item_id":"100055","item_brand":"Metzgerei Lotter","item_list_id":"category_","item_category":"BBQ","item_name":"Lammracks","item_variant":"","item_list_name":"Category: "},{"price":11.27,"index":1,"item_id":"5513","item_brand":"Metzgerei Lotter","item_list_id":"category_","item_category":"BBQ","item_name":"Steaks aus der Lammkeule","item_variant":"","item_list_name":"Category: "}],"item_list_id":"category_"}}]');
</script>
</head>
<body></body>
</html>
"""


class TestOberpfalzBeefScraper:
    def test_parse_extracts_products(self) -> None:
        scraper = OberpfalzBeefLammScraper()
        products = scraper._parse(FIXTURE_HTML)

        assert len(products) == 2
        assert products[0].id == "100055"
        assert products[0].name == "Lammracks"
        assert products[0].price == 39.71
        assert products[1].id == "5513"
        assert products[1].name == "Steaks aus der Lammkeule"
        assert products[1].price == 11.27

    def test_parse_raises_on_missing_datalayer(self) -> None:
        scraper = OberpfalzBeefLammScraper()
        try:
            scraper._parse("<html><body>No data</body></html>")
            assert False, "Expected ValueError"
        except ValueError:
            pass
