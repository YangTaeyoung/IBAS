const path = require('path');

module.exports = {
    publicPath: '/static/src/vue/dist/', // Should be STATIC_URL + path/to/build
    outputDir: path.resolve(__dirname, '../static/src/vue/dist/'), // Output to a directory in STATICFILES_DIRS
    filenameHashing: false, // Django will hash file names, not webpack
    runtimeCompiler: true, // see: https://vuejs.org/v2/guide/installation.html#Runtime-Complier-vs-Runtime-only
    devServer: {
        writerToDist: true // Write files to disk in dev mode, so Django can serve the assets
    },
};
