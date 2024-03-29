DEBUG = true;
var trace = ( DEBUG && typeof console != "undefined" ) ? console.log : function() {};
var stock_list = [['sh000001'], ['sz399001'], ['sh000300'],['sh600898']];
var cur_fetch_stock_id = -1;
var html = '';

function get_percent(delta) {
    return parseFloat(delta * 100).toFixed(2) + '%';
};
function show_stock_info() {
    var i = 0;
    for( i = 0 ; i < stock_list.length; i++ ) {
	[id, name, cur_val, delta] = stock_list[i];
	html += '<tr><td>' + name + '</td><td>' + cur_val + '</td><td>' + delta + '</td></tr>';
    }
    //trace(html);
    html += '</table>';
    _gel('stock_info').innerHTML = html;
}

function callback_func(responseText) {
    trace(responseText);
    var script = responseText;
    var cur_stock = stock_list[cur_fetch_stock_id];
    cur_fetch_stock_id++;
    script += 'var pl=hq_str_' + cur_stock[0] + '.split(",");';
    //trace(script);
    eval(script);
    //trace(pl);
    var name = pl[0];
    var cur_val = pl[3];
    var old_val = pl[2];
    var delta = get_percent((cur_val-old_val)/old_val);
    //trace(name, cur_val, delta);
    cur_stock.push(name, cur_val, delta);
    fetch_stock_info();
}

function fetch_stock_info( ) {
    if( cur_fetch_stock_id == stock_list.length ) {
	//fetch all done
	trace('fetch done');
	show_stock_info();
	return;
    }
    var stock_id = stock_list[cur_fetch_stock_id][0];
    var url = 'http://hq.sinajs.cn/list=' + stock_id;
    _IG_FetchContent(url, callback_func);
}
function timer_func() {
    if( cur_fetch_stock_id != stock_list.length && cur_fetch_stock_id != -1) {
	//last fetch not done yet
	return;
    }
    cur_fetch_stock_id = 0;
    html = '<table border="0" cellspacing="5" cellpadding="0" style="color: red; font-size: 0.8em">';
    html += '<tr style="font-weight: bold; font-size: 1.2em;"><td>名称</td>当前<td</td><td>涨跌</td></tr>';
    trace('begin to fetch stock info...');
    fetch_stock_info();

}
function init() {
    timer_func();
    var timerId = setInterval(timer_func, 1000 * 10 );
    trace('timerId is %d', timerId);
    //fetch_stock_info();

}

_IG_RegisterOnloadHandler(init);
