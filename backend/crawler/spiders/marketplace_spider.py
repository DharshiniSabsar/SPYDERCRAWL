import scrapy
from crawler.items import MarketItem


class MarketSpider(scrapy.Spider):
    name = "market"

    allowed_domains = [
        "selfhacked.com",
        "foundmyfitness.com",
        "longevity.technology",
        "lifespan.io",
        "biohackerslab.com",
        "quantifiedself.com",
        "humanos.me",
        "biohackingconference.com",
        "examine.com",
        "lesswrong.com",
        "ncbi.nlm.nih.gov",
        "nih.gov",
        "nature.com",
        "scientificamerican.com",
        "statnews.com",
    ]

    start_urls = [
        "https://selfhacked.com/",
        "https://www.foundmyfitness.com/",
        "https://longevity.technology/",
        "https://www.lifespan.io/",
        "https://www.biohackerslab.com/",
        "https://www.quantifiedself.com/",
        "https://humanos.me/",
        "https://www.biohackingconference.com/blog/",
        "https://www.examine.com/",
        "https://www.lesswrong.com/tag/biosecurity",
        "https://www.ncbi.nlm.nih.gov/pmc/",
        "https://www.nih.gov/news-events",
        "https://www.nature.com/subjects/biotechnology",
        "https://www.scientificamerican.com/biotechnology/",
        "https://www.statnews.com/tag/biotechnology/",
    ]

    # 🔑 Biohacking keyword set (lowercased for fast matching)
    BIO_KEYWORDS = {
        "biohacking", "human optimization", "quantified self",
        "longevity hacking", "sleep hacking", "cognitive enhancement",
        "metabolic optimization", "stress resilience", "health hacking",
        "body hacking", "gene editing", "crispr kits", "diy genetics",
        "synthetic biology", "gene therapy", "stem cells",
        "telomere extension", "mitochondrial enhancement",
        "rna interference", "genetic enhancement",
        "nootropics", "nootropic stacks", "racetams", "modafinil",
        "microdosing", "peptide therapy", "experimental peptides",
        "neurostimulation", "brain stimulation", "tdcs",
        "diy bio", "home lab", "wet lab", "garage biology",
        "biohacker lab", "pcr kits", "bacterial culture",
        "lab equipment", "biolab access",
        "underground biohacking", "black market", "illegal crispr",
        "rogue biolab", "human experimentation",
        "biohacking market", "darknet biotech", "illicit biotech",
        "synthetic pathogens", "gain-of-function",
        "biohacking forum", "darknet vendors", "bio vendors",
        "biotech market", "onion services", "encrypted groups",
        "private channels", "anonymous labs",
        "cyber biosecurity", "biosecurity intel",
        "biotech threats", "biological osint",
        "dual use", "bio risk", "genomic leaks", "biotech misuse",
    }

    async def start(self):
        for url in self.start_urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        self.logger.info("Scanning page: %s", response.url)

        # 🧠 Extract visible text
        page_text = " ".join(
            response.css("body *::text").getall()
        ).lower()

        # 🔍 Keyword matching
        matched_keywords = [
            kw for kw in self.BIO_KEYWORDS if kw in page_text
        ]

        # ❌ Skip pages with no biohacking relevance
        if not matched_keywords:
            return

        # ✅ Yield ONE item per relevant page
        yield MarketItem(
            title=response.css("title::text").get(),
            description="Matched keywords: " + ", ".join(matched_keywords[:10]),
            price="N/A",
            vendor=response.url.split("/")[2],
            url=response.url + "#biohacking",
        )

        # 🔁 Follow internal links (controlled)
        for href in response.css("a::attr(href)").getall():
            yield response.follow(href, callback=self.parse)
