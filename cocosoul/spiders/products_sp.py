import scrapy


class ProductsSpider(scrapy.Spider):
    name = "coco"
    allowed_domains = ["mycocosoul.com"]
    start_urls = ["https://mycocosoul.com/"]

    def parse(self, response):

        links = response.css('body > section.everything-here > div.everything-here__cont')

        links_category = []

        for l in links:
            title = l.css(' a > p::text').extract()
            category_page_url = l.css('a::attr(href)').extract()


            yield {
                'Category Title':title,
                'category_url_pages':category_page_url
            }

        for cat_prod in links.css('a::attr(href)').extract():
            print(cat_prod)
            abs_url = f"https://mycocosoul.com/{cat_prod}"
            print("the abs url spage", abs_url)
            yield scrapy.Request(url=abs_url, callback=self.products_parse)


    def products_parse(self, response):
        all_products = response.css('#skuscontainer')
        
        for prod in all_products:
            name = prod.css('div > div.product__cont__list__row > a::attr(title)').extract()
            image_product = prod.css('div > a > img::attr(src)').extract()
            prod_price = prod.css('div > div.product__cont__list__row > a.product__cont__list__two-column > div.product__cont__list__price > p.product__cont__list__price__discount::text').extract()

            print("the image" , image_product)
            print("the price" , prod_price)

            yield {
                'product_name':name,
                'product_image':image_product,
                'product_price':prod_price,
            }
