Array.prototype.inArray = function (value) {
    var i;
    for (i=0; i < this.length; i++) {
        if (this[i] === value) {
            return true;
        }
    }
    return false;
}; 

var imgWidth = '160';
if (__device == 'st') {
	imgWidth = '156';
}

var amazonUrlPrefix = "http://www.amazon.cn/gp/product/";
var amazonUrlSuffix = "?tag=shuowen-23";

var amazonProducts = [
	
//	['B0026N9OKG', '说文解字(附检字)(竖排繁体版) [平装] - 许慎', 'http://ec4.images-amazon.com/images/I/51vNZr6z0eL._AA' + imgWidth + '_.jpg'],
//	['B0019YPO66', '说文解字注(套装上下册) [精装] - 段玉裁', 'http://ec4.images-amazon.com/images/I/412Q9NSicnL._AA' + imgWidth + '_.jpg'],
//	['B005VM96KW', '说文解字句读 [精装] - 王筠', 'http://ec4.images-amazon.com/images/I/41dM2PqP0ZL._AA' + imgWidth + '_.jpg'],
//	['B005543EWW', '说文解字义证(繁体竖排版)(套装上下册) [精装] - 桂馥', 'http://ec4.images-amazon.com/images/I/41zU9MGTjpL._AA' + imgWidth + '_.jpg'],
//	['B0057S8QJC', '说文通训定声 [精装] - 朱骏声', 'http://ec4.images-amazon.com/images/I/41DHjeMC3rL._AA' + imgWidth + '_.jpg'],
//	['B0065Z5Y9Q', '说文解字系传(附检字) [精装] - 徐锴', 'http://ec4.images-amazon.com/images/I/41URBxYU0-L._AA' + imgWidth + '_.jpg']

	['B00E95ZMMI', '说文解字(附音序笔画检字)', 'http://ec4.images-amazon.com/images/I/51cGa73V%2BxL._AA' + imgWidth + '_.jpg'],
	['B0011B13W6', '广雅疏证(附索引) [精装]', 'http://ec4.images-amazon.com/images/I/41HzDUdm-jL._AA' + imgWidth + '_.jpg'],
	['B005543EWW', '说文解字义证(繁体竖排版)(套装上下册) [精装]', 'http://ec4.images-amazon.com/images/I/41zU9MGTjpL._AA' + imgWidth + '_.jpg'],
	['B0011A7SMG', '说文解字系传(精装) [精装]', 'http://ec4.images-amazon.com/images/I/51eOdja155L._AA' + imgWidth + '_.jpg'],
	['B0057S8QJC', '说文通训定声 [精装]', 'http://ec4.images-amazon.com/images/I/41DHjeMC3rL._AA' + imgWidth + '_.jpg'],
	['B005VM96KW', '说文解字句读 [精装]', 'http://ec4.images-amazon.com/images/I/41dM2PqP0ZL._AA' + imgWidth + '_.jpg'],
	['B005VM96XO', '说文释例 [精装]', 'http://ec4.images-amazon.com/images/I/51n4GvHkHeL._AA' + imgWidth + '_.jpg'],
	['B0036ZBNPM', '章太炎说文解字授课笔记(缩印本•繁体竖排版) [精装]', 'http://ec4.images-amazon.com/images/I/41h%2BUtYBhxL._AA' + imgWidth + '_.jpg'],
	['B0011FBCFK', '说文解字 [精装]', 'http://ec4.images-amazon.com/images/I/51RHuMpQ4tL._AA' + imgWidth + '_.jpg'],
	['B0011CFWR2', '黄侃手批说文解字 [精装]', 'http://ec4.images-amazon.com/images/I/51hz-dPsurL._AA' + imgWidth + '_.jpg'],
	['B00378M71W', '说文解字(现代版)(附光盘2张) [精装]', 'http://ec4.images-amazon.com/images/I/51gHtXmOcdL._AA' + imgWidth + '_.jpg'],
	['B00119CE4Y', '说文解字校订本 [精装]', 'http://ec4.images-amazon.com/images/I/41KqJM59MYL._AA' + imgWidth + '_.jpg'],
	['B005JJG7WC', '说文解字(最新整理全注全译本)(套装共5册) [精装]', 'http://ec4.images-amazon.com/images/I/51U1z2zJxVL._AA' + imgWidth + '_.jpg'],
	['B001EJUDIK', '说文解字注 [精装]', 'http://ec4.images-amazon.com/images/I/41aZ1ZDV92L._AA' + imgWidth + '_.jpg'],
	['B00112Y4R6', '古文字类编 [平装]', 'http://ec4.images-amazon.com/images/I/51JVvNXr9LL._AA' + imgWidth + '_.jpg'],
	['B0011BCS4I', '中国古文字学通论 [平装]', 'http://ec4.images-amazon.com/images/I/61V6YFx1oJL._AA' + imgWidth + '_.jpg'],
	['B002GHBPGS', '古文字诂林(全套12册) [精装]', 'http://ec4.images-amazon.com/images/I/51q0gNnqpbL._AA' + imgWidth + '_.jpg'],
	['B004IJO52I', '古文字释要 [精装]', 'http://ec4.images-amazon.com/images/I/41lS9hYPWLL._AA' + imgWidth + '_.jpg'],
	['B0011FEUUO', '古文字谱系疏证(全4册) [平装]', 'http://ec4.images-amazon.com/images/I/414de8n7ibL._AA' + imgWidth + '_.jpg']
];

function getAd() {
	
	var maxNum = 4;
	if (__device == 'pc') {
		maxNum = 6;
	}
	
	var ads = [];
	ads.push(amazonProducts[0]);
	while (ads.length < maxNum) {
		var currentAd = Math.floor(Math.random() * amazonProducts.length + 1) - 1;
		if (!ads.inArray(amazonProducts[currentAd])) {
			ads.push(amazonProducts[currentAd]);
		}
	}

	var url = '';
	var width = 'span' + (12 / maxNum);
	var html = '<div class="row-fluid"><ul class="thumbnails">';
	for (var i=0; i < ads.length; i++) {
		var cls = width;
		if (i == 0) { cls += " first" }
		url = amazonUrlPrefix + ads[i][0] + amazonUrlSuffix;
		html += '<li class="' + cls + '">';
		html += '<a class="thumbnail" target="_blank" href="' + url + '"><img src="' + ads[i][2] + '"></a>';
		html += '<a class="title" target="_blank" href="' + url + '">' + ads[i][1] + '</a>';
		html += '</li>';
	}
	html += '</ul></div>';
	return html;
}

