// metro.config.cjs
const { getDefaultConfig } = require('@expo/metro-config');

module.exports = (async () => {
  const defaultConfig = await getDefaultConfig(__dirname);
  
  // Add additional asset extensions if needed
  defaultConfig.resolver.assetExts.push('png', 'jpg', 'jpeg');

  return {
    ...defaultConfig,
    resolver: {
      ...defaultConfig.resolver,
      sourceExts: [...defaultConfig.resolver.sourceExts, 'cjs'],
    },
  };
})();
