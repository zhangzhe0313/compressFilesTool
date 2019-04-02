var gulp = require('gulp');
var livereload = require('gulp-livereload'), // 网页自动刷新（文件变动后即时刷新页面）
	webserver = require('gulp-webserver'), // 本地服务器
	uglify = require('gulp-uglify'),
	pump = require('pump'),
	runSequence = require('run-sequence'),
	browserSync = require('browser-sync').create(),
	rename = require('gulp-rename'),
	minifyCSS = require('gulp-clean-css'),
    spritesmith = require('gulp.spritesmith'),
    cache = require('gulp-cache'),
    imagemin = require('gulp-imagemin'), //压缩图片
    notify = require('gulp-notify');

var path = require('path'),
	fileConfig = require('./fileConfig.json'),
	filePath = fileConfig.fileUrl,
	dirPath = fileConfig.dirUrl,
	outputDir = fileConfig.outputDir;

// 单文件压缩
gulp.task('uglySingleJs', function (cp) {
	var stream = gulp.src([filePath])
		.pipe(uglify({
			compress: true
		}))
		.pipe(rename({suffix:'.min'}))
		.pipe(gulp.dest(outputDir))

	console.log('single js处理完毕');
	return stream;
})

//多文件压缩，文件目录
gulp.task('uglyMultyJs', function (cp) {
	var stream = gulp.src([dirPath + '/*.js'])
		.pipe(uglify({
			compress: true
		}))
		.pipe(rename({suffix:'.min'}))
		.pipe(gulp.dest(outputDir))

	console.log('multy js 处理完毕');
	return stream;
})

gulp.task('minSingleCss', function () {
	var stream = gulp.src([filePath])
		.pipe(minifyCSS({
			compatibility: 'ie8',
			keepSpecialComments: '*'
		}))
		.pipe(rename({suffix:'.min'}))
		.pipe(gulp.dest(outputDir))

	console.log('single css 处理完毕');
	return stream;
});

gulp.task('minMultyCss', function () {
	var stream = gulp.src([dirPath + '/*.css'])
		.pipe(minifyCSS({
			compatibility: 'ie8',
			keepSpecialComments: '*'
		}))
		.pipe(rename({suffix:'.min'}))
		.pipe(gulp.dest(outputDir))

	console.log('multy css 处理完毕');
	return stream;
});

// png雪碧图处理
gulp.task('spritPng', function () {
    return gulp.src([dirPath] + '/*.png')//需要合并的所有图片的地址（尽量不要使用非png格式图片，否则可能会报错）
        .pipe(spritesmith({
            imgName: outputDir + '/sprite.png',//最终生成的那一张图片路径位置
            cssName: outputDir + '/sprite.css',//对这一张大图片的各个小图标位置和大小描述的css文件路径与位置
            padding: 5,//合并时两个图片的间距
            algorithm: 'left-right',//图标在合并后的图片上的排列方式
            cssTemplate: function (data) { //生成css的模板文件
                var arr = [];
                data.sprites.forEach(function (sprite) {
                    arr.push(".icon-" + sprite.name +
                        "{" +
                        "background-image: url('" + sprite.escaped_image + "');" +
                        "background-position: " + sprite.px.offset_x + " " + sprite.px.offset_y + ";" +
                        "width:" + sprite.px.width + ";" +
                        "height:" + sprite.px.height + ";" +
                        "}\n");
                });
                return arr.join("");
            }
        }))
        .pipe(gulp.dest(outputDir)); //css和雪碧图生成的位置
});

// 图片压缩
gulp.task('compressImages', function() {
    return gulp.src([dirPath] + '/*.*')
        .pipe(cache(imagemin({
            optimizationLevel: 3,
            progressive: true,
            interlaced: true
        })))
        .pipe(gulp.dest(outputDir))
        .pipe(notify({
            message: 'Images task complete'
        }));
});


// js prod 处理
gulp.task('prodSingleJs', function (callback) {
	runSequence('uglySingleJs')
});
gulp.task('prodMultyJs', function (callback) {
	runSequence('uglyMultyJs')
});

// css prod 处理
gulp.task('prodSingleCss', function (callback) {
	runSequence('minSingleCss')
});
gulp.task('prodMultyCss', function (callback) {
	runSequence('minMultyCss')
});

//png 雪碧图处理
gulp.task('prodPngs', function (callback) {
    runSequence('spritPng')
})

//图片压缩
gulp.task('prodCompressImgs', function (callback) {
    runSequence('compressImages')
})
