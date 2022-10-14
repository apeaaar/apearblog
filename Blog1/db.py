from app.db import mongo

sitec = mongo.siteContentsField()

sitec.objectsid = 1
sitec.SITE_URL = "www.taoyan.xyz"
sitec.SITE_TITLE = "TaoYan.xyz"
sitec.BLOG_MAX_ID = 99999999
sitec.SITE_ICP = "沪ICP备2022003348号-1"
sitec.SITE_START_TIME = "ab"
sitec.SITE_MAIL = "ab@ab.ab"
sitec.SITE_YEAR = 2022
sitec.SITE_AVATAR = "https://s1.ax1x.com/2022/07/09/jrawb8.jpg"
sitec.BeautifulSentence = "Tears are words the heart can't say. 眼泪是心里无法诉说的言辞。"
sitec.SITE_TYPE_CHINESE = "拖延是最彻底的拒绝。"
sitec.SITE_TYPE_ENGLISH = "Delay is the deadliest form of denial."
sitec.secret_route = "abbswiwdisw1921h0"
sitec.leankey = "x5pNoFp6xEVyjewAj2NeED19"
sitec.leanname = "Q2qlamaqqHqD868vvCknVS8N-9Nh9j0Va"
sitec.save()