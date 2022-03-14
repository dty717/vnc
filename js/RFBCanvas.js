var RFBCanvas = function(canvas) {
    this._canvas = canvas;
    this._context = canvas.getContext('2d');

    $(this._canvas).css({border: '1px solid red'});
};

RFBCanvas.prototype.resize = function(w, h) {
    this._canvas.width  = w;
    this._canvas.height = h;
};

//getImageData(x, y, width, height)
RFBCanvas.prototype.copyRect = function(x, y, w, h, src_x, src_y) {
	var canvas_data = this._context.getImageData(src_x,src_y,w,h);
	this._context.putImageData(canvas_data, x, y);
};

RFBCanvas.prototype.drawRect = function (x_offset, y_offset, w, h, rgba_data, encodingType, configInit) {
	//rgb_decoded = Base64.decodeStr(rgba_data);
    if (encodingType == 0) {//row data

        var canvas_data = this._context.createImageData(w, h);

        for (var x = 0; x < w; x++) {
            for (var y = 0; y < w; y++) {
                var idx = (x + y * w) * 4;
                var index = (x + y * w) * 2;
                var r,g,b,a;

                if(configInit._true_color_flag){
                    if(!configInit._big_endian_flag){
                        var pixValue = (rgba_data[index+1]<<8)+(rgba_data[index]&0xff);
                        r = ((pixValue >> configInit._red_shift) & configInit._red_max) * 255 / configInit._red_max;
                        g = ((pixValue >> configInit._green_shift) & configInit._green_max) * 255 / configInit._green_max;
                        b = ((pixValue >> configInit._blue_shift) & configInit._blue_max) * 255 / configInit._blue_max;
                    }
                    a = 0xff;            
                }

                //if(a === 0)
                //	return;

                canvas_data.data[idx + 0] = r;
                canvas_data.data[idx + 1] = g;
                canvas_data.data[idx + 2] = b;
                canvas_data.data[idx + 3] = a;
            }
        }
        this._context.putImageData(canvas_data, x_offset, y_offset);

    } else {
        var canvas_data = this._context.createImageData(w, h);

        for (var x = 0; x < w; x++) {
            for (var y = 0; y < w; y++) {
                var idx = (x + y * w) * 4;
                //var b = rgba_data.charCodeAt(idx + 0);
                //var g = rgba_data.charCodeAt(idx + 1);
                //var r = rgba_data.charCodeAt(idx + 2);
                //var a = rgba_data.charCodeAt(idx + 3);


                var b = rgba_data[idx + 0];
                var g = rgba_data[idx + 1];
                var r = rgba_data[idx + 2];
                var a = rgba_data[idx + 3];
                //if(a === 0)
                //	return;

                canvas_data.data[idx + 0] = r;
                canvas_data.data[idx + 1] = g;
                canvas_data.data[idx + 2] = b;
                canvas_data.data[idx + 3] = a;
            }
        }
        this._context.putImageData(canvas_data, x_offset, y_offset);
    }


};
