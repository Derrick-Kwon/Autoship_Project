const { defineConfig } = require('@vue/cli-service')
module.exports = defineConfig({
  transpileDependencies: true
})

const { ProvidePlugin } = require("webpack");
const { BundleAnalyzerPlugin } = require("webpack-bundle-analyzer");
module.exports = defineConfig({
  devServer: {
    proxy: {
      "/api": {
        target: "http://127.0.0.1:5000"
      },
      // "/weather": {
      //   target: "https://apihub.kma.go.kr/api/typ01/url/sea_obs.php?stn=0&help=1&authKey=r6zpsnyoT4ys6bJ8qF-MCw",
      //   pathRewrite: { '^weather': '' },
      //   changeOrigin: true,
      // }
    },
  },
  transpileDependencies: true,
  lintOnSave: false,
  configureWebpack: (config) => {
    config.devtool = "source-map";
    config.resolve.symlinks = false;
    config.resolve.fallback = {
      crypto: false, // crypto-browserify can be polyfilled here if needed
      stream: false, // stream-browserify can be polyfilled here if needed
      assert: false, // assert can be polyfilled here if needed
      os: false, // os-browserify can be polyfilled here if needed
      https: false, // https-browserify can be polyfilled here if needed
      http: false, // stream-http can be polyfilled here if needed
      url: false, // url can be polyfilled here if needed
      zlib: false, // browserify-zlib can be polyfilled here if needed
      fs: false,
      net: false,
      tls: false,
      timers: false,
    };
    config.plugins.push(new ProvidePlugin({ Buffer: ["buffer", "Buffer"] }));
    config.plugins.push(new ProvidePlugin({ process: ["process/browser"] }));
    config.plugins.push(
      new BundleAnalyzerPlugin({
        analyzerMode: "disabled",
      })
    );
  },
})