var gulp = require('gulp');
var livereload = require('gulp-livereload'), // 网页自动刷新（文件变动后即时刷新页面）
	webserver = require('gulp-webserver'), // 本地服务器
	uglify = require('gulp-uglify'),
	pump = require('pump'),
	runSequence = require('run-sequence'),
	browserSync = require('browser-sync').create(),
	rename = require('gulp-rename'),
	minifyCSS = require('gulp-clean-css');

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
