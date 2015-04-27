var doX = function(s) {
    // according to python html.escape
    var escaped = s.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');

    // \r should not already appear
    var furtherescaped = escaped.replace(/\n/g, '<br>\n').replace(/\ /g, '&nbsp;').replace(/\t/g, '&nbsp;&nbsp;&nbsp;&nbsp;');
    return furtherescaped;
}

var unX = function(s) {
    // just opposite to doX
    var unfurther = s.replace(/&nbsp;&nbsp;&nbsp;&nbsp;/g, '\t').replace(/&nbsp;/g, ' ').replace(/<br>\n/g, '\n');
    var unx = unfurther.replace(/&lt;/g, '<').replace(/&gt;/g, '>').replace(/&amp;/g, '&');
    return unx;
}


$.fn.highlightRange = function(start, end) {
    var e = $(this); //= document.getElementById($(this).attr('id')); // I don't know why... but $(this) don't want to work today :-/
    var offset = start;
    var length = end - start + 1;
    var el = e.get(0);
    var unhtml = window.source0; // unescape it to make offsets actual
    var vre = doX(unhtml.substr(0, offset)) +
        '<span class="highlight">' +
        doX(unhtml.substr(offset, length)) +
        "</span>" +
        doX(unhtml.substr(offset + length));
    el.innerHTML = vre;
    return $(this);
}

$.fn.lowlight = function() {
    $(this).html(window.source0);
    return $(this);
}

$.fn.scrollXY = function(scx, scy) {
    var th = $(this);
    var e = th.get(0);
    e.scrollLeft = scx;
    e.scrollTop = scy;
    return th;
}

$(document).ready(function() {

    var clog = function(msg) {
        if(window.qtab)
            qtab.clog(msg);
        else
            console.log(msg);
    };

    var highlightRange = function(hls, hle) {
        if (window.qtab) {
            qtab.src_select(hls, hle);
        } else {
            $('div#source code').highlightRange(hls, hle);
        }
    };

    var lowlight = function() {
        if (window.qtab) {
            qtab.src_select(0, 0);
        } else {
            $('div#source code').lowlight();
        }
    };

    var curtr = undefined;
    $('.variative').mouseenter(function() {
        if(!window.qtab) curtr = $(this);
    });

    $('.multiple').attr('contextmenu', 'multiplemenu');
    $('.single').attr('contextmenu', 'singlemenu');

    var commoncontext = function(ctr) {
        ctr.css("background-color", "lightgrey").removeAttr('contextmenu');
        var datagroups = ctr.attr("data-groups");
        var bdl = $('#black_descriptor_list');
        bdl.html(bdl.html() + datagroups + "\n");
        return datagroups;
    };

    var saveInfDicts = function() {
        var te = $('#toelem_descriptor_list').html();
        var td = $('#todict_descriptor_list').html();
        if (window.qtab) {
            qtab.inf_dic_descs(te, td);
        } else {
            clog([te, td].toString());
        }
    }

    window.decide_enable_dict = function(x, y) {
        clog("Context menu on: (" + x + "," + y + ")")
        var elt = document.elementFromPoint(x, y);
        var tr = $(elt).closest('tr.variative');
        curtr = tr;
        if(tr.hasClass("single")) {
            clog("... single...");
            qtab.enable_dict(true);
        } else {
            clog("... multiple...");
            qtab.enable_dict(false);
        }
    }

    window.single2dict = function() {
        clog("#single2dict");
        var dg = commoncontext(curtr);
        var targ = $('#todict_descriptor_list');
        targ.html(targ.html() + dg + "\n");
        saveInfDicts();
        if(window.qtab) {
            window.qtab.refactor_create_dic_entry(dg)
        }
    };

    var single2elem = function() {
        clog("#single2elem");
        var dg = commoncontext(curtr);
        var targ = $('#toelem_descriptor_list');
        targ.html(targ.html() + dg + "\n");
        saveInfDicts();
        if(window.qtab) {
            window.qtab.refactor_create_inf_elt(dg)
        }
    };

    var multiple2elem = function() {
        clog("#multiple2elem");
        var dg = commoncontext(curtr);
        var targ = $('#toelem_descriptor_list');
        targ.html(targ.html() + dg + "\n");
        saveInfDicts();
        if(window.qtab) {
            window.qtab.refactor_create_inf_elt(dg)
        }
    };

    window.some2elem = function() {
        if (curtr.hasClass("single"))
            single2elem();
        else
            multiple2elem();
    }

    $("#single2dict").click(single2dict);
    $("#single2elem").click(single2elem);
    $("#multiple2elem").click(multiple2elem);

    $('.variationclick').click(function() {
        var hlrange = $(this).attr("data-hlrange").split('-');
        var hls = +hlrange[0];
        var hle = +hlrange[1];
        var src = $('div#source code');
        lowlight();
        highlightRange(hls, hle);

        if (!window.qtab) {
            src.parent().scrollXY(0, 0); // to calculate $('span.highlight').offset().top later properly
            src.parent().scrollXY(0, $('span.highlight').offset().top)
        }
    });

    window.source0 = $('div#source code').get(0).textContent; // unescapes

    window.adaptToQWebView = function() {
        clog("Adapting to QWebView!");
        $("#removeforqwebview").remove();
        // window.qtab.src_text(window.source0) // Qt will load source itself
        $('span#srclabel').remove();
        $('div#source code').empty();
        $('div#source').hide();
        $('body').css({
            'overflow': 'hidden'
        });
        correct_sizes();
    }

    var correct_sizes = function() {
        var tb = $("tbody")[0];
        var scrollbarw = tb.offsetWidth - tb.clientWidth;
        // alert(scrollbarw);
        var fxd = 100
        var wh = window.innerHeight;
        var ww = window.innerWidth;

        var thh = $('div#table thead').height();

        if (window.qtab) {
            // thh += 4; // impirically
            $("tbody").height(wh - thh);
            $("div#table").height(wh);
        } else {
            var sh = $('span#srclabel').height();
            $("tbody").height(wh * 0.6 - thh - sh);
            $("div#table").height(wh * 0.6 - thh);
            $("div#source").height(wh * 0.4);
        }

        $("th.fxd, td.fxd").width(fxd);

        var thl = $("th.tka").offset().left;
        var sbs = scrollbarw * 1; // impirically...

        $("th.tka").width(ww - thl);
        $("td.tka").width(ww - sbs - thl);
    };

    $(window).resize(correct_sizes);
    correct_sizes();

    // window.adaptToQWebView(); // uncomment to debug in browser
});
