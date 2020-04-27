// const gulp = require('gulp');
// const concat = require('gulp-concat');
// const { series, parallel } = require('gulp');
// const child = require('child_process');
// const gutil = require('gulp-util');
// const uglify = require('gulp-uglify');
// const sass = require('./build/sass');
// const imagemin = require('gulp-imagemin');
// const scripts = require('./build/scripts');
// const images = require('./build/images');
// const sync = require('./build/browsersync');


// gulp.task('scripts', function() {
//   return gulp.src(src + 'js/*.js')
//     .pipe(concat('main.js'))
//       .pipe(rename({suffix: '.min'}))
//       .pipe(uglify())
//       .pipe(gulp.dest(dest + 'js'));
// });
// // Compile CSS from Sass files
// gulp.task('sass', function() {
//   return sass('_scss/*.scss', {style: 'compressed'})
//       .pipe(rename({suffix: '.min'}))
//       .pipe(gulp.dest('build/css'));
// });
// gulp.task('images', function() {
// return gulp.src(src + 'img/**/*.+(png|jpg|gif|svg)')
//   .pipe(cache(imagemin({ optimizationLevel: 5, progressive: true, interlaced: true })))
//   .pipe(gulp.dest(dest + 'img'));
// });

// gulp.task('browser-sync', function() {
//   bs.init({
//       server: {
//           baseDir: "./"
//       }
//   });
// });

// gulp.task('default', async function() { return gulp.series(gulp.parallel('sass', 'scripts', 'images' ))});

// gulp.task('build', async function() { return gulp.series(gulp.parallel('sass', 'scripts', 'images'))});

// // gulp.task('build', gulp.series(gulp.parallel('sass', 'scripts', 'images', 'jekyll-build')));

// // old code:   gulp.task('build', ['sass', 'scripts', 'images', 'jekyll-build']);

const gulp = require('gulp');
const sass = require('./build/sass');
const scripts = require('./build/scripts');
const images = require('./build/images');
const sync = require('./build/browsersync');

[sass, scripts, images, sync].forEach(task => {
  task(gulp);
});

gulp.task( 'default', [ 'serve' ] );

gulp.task('build', ['sass', 'scripts', 'images', 'jekyll-build']);