from django.db import models


class Constants:
    class InvestmentType(models.TextChoices):
        """
        We want enumeration for investment type as there is only a set, finite number of choices.
        """

        SHARES = ("Shares", "Shares")
        CRYPTO = ("Crypto", "Crypto")

    class Exchanges(models.TextChoices):
        """ 
        The exchanges around the world that can be used to buy and sell shares.
        """

        XASX = ("XASX", "ASX")
        XAMS = ("XAMS", "AMS")
        XBOM = ("XBOM", "BOM")
        XBRU = ("XBRU", "BRU")
        XFRA = ("XFRA", "FRA")
        XHKG = ("XHKG", "HKG")
        XJPX = ("XJPX", "JPX")
        XKOS = ("XKOS", "KOS")
        XLIS = ("XLIS", "LIS")
        XLON = ("XLON", "LON")
        XMIL = ("XMIL", "MIL")
        XMSM = ("XMSM", "MSM")
        XNAS = ("XNAS", "NAS")
        XNSE = ("XNSE", "NSE")
        XNYS = ("XNYS", "NYS")
        XOSL = ("XOSL", "OSL")
        XSAU = ("XSAU", "SAU")
        XSHE = ("XSHE", "SHE")
        XSHG = ("XSHG", "SHG")
        XSWX = ("XSWX", "SWX")
        XTAI = ("XTAI", "TAI")
        XTSE = ("XTSE", "TSE")

    class Platforms(models.TextChoices):
        """ 
        The exchanges around the world that can be used to buy and sell shares.
        """

        CMC = ("CMC", "CMC")
        LINK = ("LINK", "LINK")
        BOARDROOM = ("BOARDROOM", "BOARDROOM")
        DIRECT = ("DIRECT", "DIRECT")
        IPO = ("IPO", "IPO")

    class Currencies(models.TextChoices):
        """
        We want enumeration for investment type as there is only a set, finite number of choices.
        """

        AUD = ("AUD", "AUD")
        USD = ("USD", "USD")
