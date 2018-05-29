/*!
 * jQuery Cookie Plugin v1.3.1
 * https://github.com/carhartl/jquery-cookie
 *
 * Copyright 2013 Klaus Hartl
 * Released under the MIT license
 */
(function (factory) {
	if (typeof define === 'function' && define.amd) {
		// AMD. Register as anonymous module.
		define(['jquery'], factory);
	} else {
		// Browser globals.
		factory(jQuery);
	}
}(function ($) {

	var pluses = /\+/g;

	function raw(s) {
		return s;
	}

	function decoded(s) {
		return decodeURIComponent(s.replace(pluses, ' '));
	}

	function converted(s) {
		if (s.indexOf('"') === 0) {
			// This is a quoted cookie as according to RFC2068, unescape
			s = s.slice(1, -1).replace(/\\"/g, '"').replace(/\\\\/g, '\\');
		}
		try {
			return config.json ? JSON.parse(s) : s;
		} catch(er) {}
	}

	var config = $.cookie = function (key, value, options) {

		// write
		if (value !== undefined) {
			options = $.extend({}, config.defaults, options);

			if (typeof options.expires === 'number') {
				var days = options.expires, t = options.expires = new Date();
				t.setDate(t.getDate() + days);
			}

			value = config.json ? JSON.stringify(value) : String(value);

			return (document.cookie = [
				config.raw ? key : encodeURIComponent(key),
				'=',
				config.raw ? value : encodeURIComponent(value),
				options.expires ? '; expires=' + options.expires.toUTCString() : '', // use expires attribute, max-age is not supported by IE
				options.path    ? '; path=' + options.path : '',
				options.domain  ? '; domain=' + options.domain : '',
				options.secure  ? '; secure' : ''
			].join(''));
		}

		// read
		var decode = config.raw ? raw : decoded;
		var cookies = document.cookie.split('; ');
		var result = key ? undefined : {};
		for (var i = 0, l = cookies.length; i < l; i++) {
			var parts = cookies[i].split('=');
			var name = decode(parts.shift());
			var cookie = decode(parts.join('='));

			if (key && key === name) {
				result = converted(cookie);
				break;
			}

			if (!key) {
				result[name] = converted(cookie);
			}
		}

		return result;
	};

	config.defaults = {};

	$.removeCookie = function (key, options) {
		if ($.cookie(key) !== undefined) {
			// Must not alter options, thus extending a fresh object...
			$.cookie(key, '', $.extend({}, options, { expires: -1 }));
			return true;
		}
		return false;
	};

}));


var __chars = [];
var __device = jQuery.cookie('d');

// 生成收藏数据
function generateFavorite(data) {
	var selected = [];
	var html = '<ul>';
	for (var i in data) {
		
		var c = data[i];
		if (typeof c == 'function') {
			continue;
		}
		
		var ga = ' ga-event="favorite|remove|' + c['i'] + '|' + c['z'] + '"';
		
		// 生成收藏内容
		html += '<li class="fav">';
		
		html += '<a href="' + c['u'] + '"';
		html += ' title="查看【' + c['z'] + '】的詳細信息">' + c['z'] + '</a>';
		
		html += '<a href="' + c['r'] + '" rel="nofollow" class="remove" ';
		html += ' title="删除看【' + c['z'] + '】"' + ga + '>x</a>';
		
		html += '</li>';
		
		// 加入已选择列表
		selected.push(c['i']);
		
		// 禁用收藏链接
		var el = $('#fav' + c['i'] + ' a');
		if (el) {
			var ga = ' ga-event="favorite|add|' + c['i'] + '|' + c['z'] + '"';
			
			if (el.hasClass('detail')) {
				el.replaceWith('<span class="muted detail" data-url="' + el.attr('href') + '"' + ga + '>加入收藏</span>');
			} else {
				el.replaceWith('<span class="muted" data-url="' + el.attr('href') + '"' + ga + '>收藏</span>');
			}
		}
	}
	
	html += '</ul>';
	
	// 显示收藏列表
	$('#favoriteChars').html(html);

	// 激活收藏链接
	for (var i in __chars) {
		if (typeof __chars[i] == 'function' || selected.inArray(__chars[i])) {
			continue;
		}
		var span = $('#fav' + __chars[i] + ' span.muted');
		if (span.length == 1 && span.attr('data-url')) {
			var isDetail = span.hasClass('detail');
			var cls = isDetail?'class="detail"':'';
			var txt = isDetail?'加入收藏':'收藏';
			var ga = span.attr('ga-event')?' ga-event="' + span.attr('ga-event') + '"':'';
			var link = '<a ' + cls + ga + ' href="' + span.attr('data-url') + '">' + txt + '</a>';
			$('#fav' + __chars[i] + ' span.muted').replaceWith(link);
		}
	}
}

(function checkWindowSize() {
	var width = (window.innerWidth 
		|| ((document.documentElement.clientWidth - document.documentElement.clientLeft) 
			|| document.body.clientWidth));
	var width = Math.max(jQuery(window).innerWidth(), width);
	var device = '';
	if (width >= 1200) {
		device = 'pc';
	} else if (width < 1200 && width >= 980) {
		device = 'tb';
	} else if (width < 980 && width >= 768) {
		device = 'st';
	} else if (width < 768 && width >= 480) {
		device = 'mb';
	} else if (width < 480) {
		device = 'mb';
	} else {
		device = 'tb';
	}

	if (__device != device) {
		__device = device;
		var hostname = window.location.hostname.substring(3);
		jQuery.cookie('d', device, { expires: 365, path: '/' });
		window.location = window.location;
	}
})();

jQuery(document).ready(function($){
	
	// 获取当前页面的字符
	$('.fav').each(function() {
		var id = $(this).attr('id');
		if (!id) {
			return;
		}
		id = id.replace('fav', '');
		__chars.push(parseInt(id));
	});

	// 获取页脚广告
	$('#footerAd').html(getAd());
	
	// 加载收藏
	$.ajax({
		url: '/favorite/my',
		cache: false,
		dataType: 'json'
	}).done(function(data) {
		generateFavorite(data);
	});
	
	// 处理收藏链接 & GA 点击事件
	$(document).on("click", ".fav a, a.fav", function() {
		
		var ga = $(this).attr('ga-event');
		if (ga && _gaq) {
			var parts = ga.split("|");
			if (parts.length == 4) {
				_gaq.push(['_trackEvent', parts[0], parts[1], parts[2] + ':' + parts[3]]);
			} else if (parts.length == 2) {
				_gaq.push(['_trackEvent', parts[0], parts[1]]);
			}
		}
		
		var linkHref = $(this).attr('href');
		$.ajax({
			url: linkHref,
			cache: false,
			dataType: 'json'
		}).done(function(data) {
			generateFavorite(data);
		});
		
		return false;
	});
	
	// 显示字符集提示
	if (!$.cookie('w')) {
		
		$charWarning = '<div class="alert alert-info">'
			+ '<button class="close" data-dismiss="alert" type="button">×</button>'
			+ '<strong>提示信息:</strong>'
			+ '為確保準確地顯示本網站裏所有字符，請首先安裝包括 Unicode CJK Extension A 和 B 的字符集並把瀏覽器的字符集編碼設置為 UTF8。'
			+ '</div>';

		$('#main').prepend($charWarning);
		
		$.cookie('w', 1, { expires: 365, path: '/' });
	}
});