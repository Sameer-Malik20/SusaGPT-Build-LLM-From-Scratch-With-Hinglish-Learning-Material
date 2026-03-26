# 🔧 Build Tools & CI/CD - Modern Frontend Development Pipeline
> **Level:** Intermediate → Expert | **Language:** Hinglish | **Goal:** Frontend build tools, bundlers, aur CI/CD pipelines master karna

---

## 🧭 Core Concepts (Concept-First)

- Build tools: bundlers (Webpack, Vite), transpilation, and asset processing.
- Code quality: linting, formatting, type checks, and pre-commit hooks.
- CI/CD: pipelines, automated tests, build, and deployment steps.
- Caching and performance: cache wipes, persistent caches, and reproducible builds.
- Environment parity: different envs (dev/stage/prod) and feature flags.
- Observability: logs, metrics, and error reporting for deployments.

---

## 📋 Table of Contents: Development Pipeline

| Stage | Tools | Purpose |
|-------|-------|---------|
| **Development** | Vite, Webpack, Parcel | Local development environment |
| **Bundling** | esbuild, Rollup, SWC | Code optimization aur bundling |
| **Testing** | Jest, Cypress, Playwright | Quality assurance aur testing |
| **CI/CD** | GitHub Actions, Jenkins, CircleCI | Automated deployment pipeline |
| **Deployment** | Vercel, Netlify, AWS Amplify | Production hosting aur deployment |

---

## 1. 🛠️ Development Tools

### A. Module Bundlers Comparison

#### 1. **Webpack** (The Industry Standard)
- **Strengths:** Extensive plugin ecosystem, Code splitting
- **Use Case:** Large enterprise applications

```javascript
// webpack.config.js
module.exports = {
  entry: './src/index.js',
  output: {
    filename: 'bundle.js',
    path: path.resolve(__dirname, 'dist'),
  },
  module: {
    rules: [
      {
        test: /\.js$/,
        exclude: /node_modules/,
        use: 'babel-loader',
      },
      {
        test: /\.css$/,
        use: ['style-loader', 'css-loader'],
      },
    ],
  },
  plugins: [
    new HtmlWebpackPlugin({
      template: './src/index.html',
    }),
  ],
};
```

#### 2. **Vite** (Modern Fast Alternative)
- **Strengths:** Lightning fast development server, Native ES modules
- **Use Case:** Modern frameworks (React, Vue, Svelte)

```javascript
// vite.config.js
import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';

export default defineConfig({
  plugins: [react()],
  server: {
    port: 3000,
    open: true,
  },
  build: {
    outDir: 'dist',
    sourcemap: true,
  },
});
```

#### 3. **esbuild** (Extremely Fast)
- **Strengths:** Written in Go, 10-100x faster than Webpack
- **Use Case:** Simple projects, Build tool for other bundlers

```javascript
// esbuild.config.js
import esbuild from 'esbuild';

esbuild.build({
  entryPoints: ['src/index.js'],
  bundle: true,
  outfile: 'dist/bundle.js',
  minify: true,
  sourcemap: true,
}).catch(() => process.exit(1));
```

### B. Development Server Features

#### Hot Module Replacement (HMR):
```javascript
// Webpack HMR configuration
devServer: {
  hot: true, // Enable HMR
  liveReload: false,
  static: './dist',
  historyApiFallback: true,
  client: {
    overlay: {
      errors: true,
      warnings: false,
    },
  },
}

// Vite automatically includes HMR
// No configuration needed
```

---

## 2. 📦 Bundling Optimization

### A. Code Splitting Strategies

#### 1. **Entry Point Splitting**
```javascript
// Multiple entry points
entry: {
  main: './src/main.js',
  vendor: './src/vendor.js',
  admin: './src/admin.js',
},

// Output configuration
output: {
  filename: '[name].[contenthash].js',
  path: path.resolve(__dirname, 'dist'),
},
```

#### 2. **Dynamic Import Splitting**
```javascript
// Dynamic imports create separate chunks
const loadComponent = async () => {
  const { default: Component } = await import('./HeavyComponent');
  return Component;
};

// Webpack magic comments for chunk naming
import(/* webpackChunkName: "heavy-component" */ './HeavyComponent');
```

#### 3. **SplitChunks Optimization**
```javascript
optimization: {
  splitChunks: {
    chunks: 'all',
    cacheGroups: {
      vendors: {
        test: /[\\/]node_modules[\\/]/,
        name: 'vendors',
        chunks: 'all',
      },
      commons: {
        name: 'commons',
        minChunks: 2,
        chunks: 'initial',
        minSize: 0,
      },
    },
  },
},
```

### B. Asset Optimization

#### Image Optimization Pipeline:
```javascript
// Using image-webpack-loader
{
  test: /\.(png|jpg|jpeg|gif|svg)$/,
  use: [
    {
      loader: 'file-loader',
      options: {
        name: '[name].[hash].[ext]',
        outputPath: 'images',
      },
    },
    {
      loader: 'image-webpack-loader',
      options: {
        mozjpeg: {
          progressive: true,
          quality: 65,
        },
        optipng: {
          enabled: false,
        },
        pngquant: {
          quality: [0.65, 0.90],
          speed: 4,
        },
        gifsicle: {
          interlaced: false,
        },
      },
    },
  ],
}
```

---

## 3. 🧪 Testing Integration

### A. Test Runner Configuration

#### Jest Setup:
```javascript
// jest.config.js
module.exports = {
  testEnvironment: 'jsdom',
  setupFilesAfterEnv: ['<rootDir>/jest.setup.js'],
  moduleNameMapper: {
    '\\.(css|less|scss|sass)$': 'identity-obj-proxy',
    '\\.(jpg|jpeg|png|gif|svg)$': '<rootDir>/__mocks__/fileMock.js',
  },
  collectCoverageFrom: [
    'src/**/*.{js,jsx}',
    '!src/**/*.test.{js,jsx}',
    '!src/index.js',
  ],
  coverageThreshold: {
    global: {
      branches: 80,
      functions: 80,
      lines: 80,
      statements: 80,
    },
  },
};
```

#### Testing in Build Pipeline:
```javascript
// package.json scripts
{
  "scripts": {
    "test": "jest",
    "test:watch": "jest --watch",
    "test:coverage": "jest --coverage",
    "test:ci": "jest --ci --coverage --maxWorkers=2",
    "lint": "eslint src/",
    "lint:fix": "eslint src/ --fix",
    "build": "npm run lint && npm run test:ci && webpack --mode production"
  }
}
```

### B. E2E Testing Integration

#### Cypress Configuration:
```javascript
// cypress.config.js
const { defineConfig } = require('cypress');

module.exports = defineConfig({
  e2e: {
    baseUrl: 'http://localhost:3000',
    specPattern: 'cypress/e2e/**/*.cy.{js,jsx,ts,tsx}',
    supportFile: 'cypress/support/e2e.js',
    viewportWidth: 1280,
    viewportHeight: 720,
    video: true,
    screenshotOnRunFailure: true,
  },
  component: {
    devServer: {
      framework: 'react',
      bundler: 'webpack',
    },
  },
});
```

---

## 4. 🔄 CI/CD Pipeline

### A. GitHub Actions Workflow

#### Complete CI Pipeline:
```yaml
# .github/workflows/ci.yml
name: CI Pipeline
on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Setup Node.js
        uses: actions/setup-node@v3
        with:
          node-version: '18'
          cache: 'npm'
      
      - name: Install dependencies
        run: npm ci
      
      - name: Lint code
        run: npm run lint
      
      - name: Run tests
        run: npm run test:ci
      
      - name: Build project
        run: npm run build
      
      - name: Upload coverage
        uses: codecov/codecov-action@v3
        with:
          file: ./coverage/lcov.info

  deploy:
    needs: test
    runs-on: ubuntu-latest
    if: github.ref == 'refs/heads/main'
    steps:
      - uses: actions/checkout@v3
      
      - name: Setup Node.js
        uses: actions/setup-node@v3
        with:
          node-version: '18'
      
      - name: Install dependencies
        run: npm ci
      
      - name: Build project
        run: npm run build
      
      - name: Deploy to Vercel
        uses: amondnet/vercel-action@v20
        with:
          vercel-token: ${{ secrets.VERCEL_TOKEN }}
          vercel-org-id: ${{ secrets.ORG_ID}}
          vercel-project-id: ${{ secrets.PROJECT_ID}}
          vercel-args: '--prod'
```

### B. Deployment Strategies

#### 1. **Blue-Green Deployment**
```yaml
# AWS CodeDeploy configuration
version: 0.0
Resources:
  - TargetService:
      Type: AWS::ECS::Service
      Properties:
        TaskDefinition: "<TASK_DEFINITION>"
        LoadBalancerInfo:
          ContainerName: "webapp"
          ContainerPort: 80
        DeploymentStyle:
          DeploymentType: BLUE_GREEN
          DeploymentOption: WITH_TRAFFIC_CONTROL
```

#### 2. **Canary Deployment**
```javascript
// Feature flag based canary deployment
const features = {
  newDashboard: {
    enabled: isCanaryUser(userId),
    percentage: 10, // 10% of users
  },
};

if (features.newDashboard.enabled) {
  renderNewDashboard();
} else {
  renderOldDashboard();
}
```

---

## 5. 🚀 Production Deployment

### A. Static Site Hosting

#### Vercel Deployment:
```json
// vercel.json configuration
{
  "builds": [
    {
      "src": "package.json",
      "use": "@vercel/static-build",
      "config": {
        "distDir": "dist"
      }
    }
  ],
  "routes": [
    {
      "src": "/(.*)",
      "dest": "/dist/$1"
    }
  ],
  "env": {
    "REACT_APP_API_URL": "https://api.example.com"
  }
}
```

#### Netlify Configuration:
```toml
# netlify.toml
[build]
  command = "npm run build"
  publish = "dist"

[build.environment]
  NODE_VERSION = "18"

[[redirects]]
  from = "/*"
  to = "/index.html"
  status = 200

[[headers]]
  for = "/*"
  [headers.values]
    X-Frame-Options = "DENY"
    X-Content-Type-Options = "nosniff"
```

### B. Performance Optimization in Production

#### Bundle Analysis:
```javascript
// webpack-bundle-analyzer
const BundleAnalyzerPlugin = require('webpack-bundle-analyzer').BundleAnalyzerPlugin;

module.exports = {
  plugins: [
    new BundleAnalyzerPlugin({
      analyzerMode: 'static',
      reportFilename: 'bundle-report.html',
      openAnalyzer: false,
    }),
  ],
};

// Run analysis
npm run build -- --analyze
```

#### Performance Budget:
```javascript
// performance-budget.js
module.exports = {
  performance: {
    maxAssetSize: 250000, // 250KB
    maxEntrypointSize: 250000,
    hints: 'error',
    assetFilter: function(assetFilename) {
      return !assetFilename.endsWith('.map');
    },
  },
};
```

---

## 6. 🔧 Advanced Configuration

### A. Environment-specific Builds

#### Webpack Environment Configuration:
```javascript
// webpack.config.js
const webpack = require('webpack');
const dotenv = require('dotenv');

module.exports = (env) => {
  // Load environment variables
  const envFile = env.production ? '.env.production' : '.env.development';
  const envConfig = dotenv.config({ path: envFile }).parsed;
  
  // Convert to webpack DefinePlugin format
  const envKeys = Object.keys(envConfig).reduce((prev, next) => {
    prev[`process.env.${next}`] = JSON.stringify(envConfig[next]);
    return prev;
  }, {});

  return {
    // ... other config
    plugins: [
      new webpack.DefinePlugin(envKeys),
    ],
  };
};
```

#### Multiple Environment Builds:
```json
{
  "scripts": {
    "build:dev": "webpack --env development",
    "build:staging": "webpack --env staging",
    "build:prod": "webpack --env production",
    "build:all": "npm run build:dev && npm run build:staging && npm run build:prod"
  }
}
```

### B. Custom Loaders and Plugins

#### Creating Custom Loader:
```javascript
// custom-markdown-loader.js
module.exports = function(source) {
  // Transform markdown to HTML
  const marked = require('marked');
  const html = marked(source);
  
  // Return as ES module
  return `export default ${JSON.stringify(html)}`;
};

// Using custom loader
{
  test: /\.md$/,
  use: [
    {
      loader: path.resolve(__dirname, 'loaders/custom-markdown-loader.js'),
    },
  ],
}
```

---

## 7. 🧪 Practical Exercises

### Exercise 1: Build Tool Migration
1. Existing Webpack project ko Vite mein migrate karo
2. Build times compare karo
3. Bundle sizes analyze karo
4. Development experience compare karo

### Exercise 2: CI/CD Pipeline Setup
1. GitHub Actions workflow create karo
2. Automated testing aur linting add karo
3. Automated deployment setup karo
4. Performance budgets enforce karo

### Exercise 3: Production Optimization
1. Bundle analysis perform karo
2. Code splitting strategies implement karo
3. Asset optimization apply karo
4. Performance metrics measure karo

---

## 📚 Resources

### Build Tools Documentation
- **Webpack:** Official documentation and guides
- **Vite:** Modern build tool documentation
- **esbuild:** Extremely fast JavaScript bundler
- **Rollup:** Next-generation module bundler

### CI/CD Platforms
- **GitHub Actions:** Integrated CI/CD solution
- **GitLab CI:** Complete DevOps platform
- **Jenkins:** Extensible automation server
- **CircleCI:** Cloud-based CI/CD platform

### Deployment Platforms
- **Vercel:** Frontend cloud platform
- **Netlify:** All-in-one platform for web projects
- **AWS Amplify:** Full-stack deployment service
- **Firebase Hosting:** Google's hosting platform

---

## 🏆 Checklist
- [ ] Different build tools compare aur choose kar sakte hain
- [ ] Code splitting strategies implement kar sakte hain
- [ ] Testing integration setup kar sakte hain
- [ ] CI/CD pipeline create kar sakte hain
- [ ] Production deployment configure kar sakte hain
- [ ] Performance optimization apply kar sakte hain
- [ ] Environment-specific builds manage kar sakte hain

> **Pro Tip:** Build tools ecosystem rapidly evolve karta hai. Regularly evaluate new tools, but don't chase every new trend. Stability aur performance balance maintain karo. Always measure before making changes.
