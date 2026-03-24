import { defineConfig, globalIgnores } from "eslint/config";
import nextVitals from "eslint-config-next/core-web-vitals";
import nextTs from "eslint-config-next/typescript";
import js from '@eslint/js';
import globals from 'globals';
import reactHooks from 'eslint-plugin-react-hooks';
import { reactRefresh } from 'eslint-plugin-react-refresh';
import { configs as tseslintConfigs } from 'typescript-eslint';
import react from 'eslint-plugin-react';
import stylistic from '@stylistic/eslint-plugin';
import simpleImportSort from 'eslint-plugin-simple-import-sort';
import { flatConfigs as importXFlatConfigs, importX } from 'eslint-plugin-import-x';

const typeCheckConfigs = [
  ...tseslintConfigs.strictTypeChecked,
  ...tseslintConfigs.stylisticTypeChecked,
].map((config) => ({
  ...config,
  files: ['**/*.{ts,tsx}'],
}));

export default defineConfig([
  globalIgnores([
    ".next/**",
    "out/**",
    "build/**",
    "next-env.d.ts",
    "dist",
    "node_modules",
    "src/lib/api/v1.d.ts",
  ]),

  js.configs.recommended,
  ...nextVitals,
  ...nextTs,
  ...typeCheckConfigs,
  importXFlatConfigs.recommended,
  importXFlatConfigs.typescript,

  {
    files: ['**/*.{ts,tsx}'],
    languageOptions: {
      ecmaVersion: 2020,
      globals: {
        ...globals.browser,
        ...globals.node,
      },
      parserOptions: {
        project: ['./tsconfig.json'],
        tsconfigRootDir: import.meta.dirname,
      },
    },
    plugins: {
      'react-hooks': reactHooks,
      'react-refresh': reactRefresh,
      react,
      '@stylistic': stylistic,
      'simple-import-sort': simpleImportSort,
      'import-x': importX,
    },
    rules: {
      ...react.configs.recommended.rules,
      ...react.configs['jsx-runtime'].rules,
      ...reactHooks.configs.recommended.rules,

      // --- Import Rules ---
      'object-curly-spacing': ['error', 'always'],
      'simple-import-sort/imports': 'error',
      'simple-import-sort/exports': 'error',
      'sort-imports': 'off',
      'import-x/extensions': ['error', 'ignorePackages', { js: 'never', jsx: 'never', ts: 'never', tsx: 'never' }],

      // --- TypeScript ---
      '@typescript-eslint/no-unused-vars': [
        'error',
        { argsIgnorePattern: '^_', varsIgnorePattern: '^_', caughtErrorsIgnorePattern: '^_' }
      ],
      'react/prop-types': 'off',
      '@typescript-eslint/no-empty-interface': 'off',
      '@typescript-eslint/no-non-null-assertion': 'off',

      // --- React Strict ---
      'react/jsx-no-leaked-render': ['error', { validStrategies: ['ternary'] }],
      'react/forward-ref-uses-ref': 'error',
      'react/no-array-index-key': 'warn',
      'react/jsx-tag-spacing': ['error', { 'beforeSelfClosing': 'always' }],

      // --- Styling ---
      '@stylistic/semi': ['error', 'always'],
      '@stylistic/quotes': ['error', 'double'],
      '@stylistic/jsx-quotes': ['error', 'prefer-double'],
      '@stylistic/comma-dangle': ['error', 'always-multiline'],
      '@stylistic/max-len': ['error', { code: 120, tabWidth: 2, ignoreUrls: true, ignoreStrings: true, ignoreTemplateLiterals: true, ignoreRegExpLiterals: true }],
      '@stylistic/jsx-max-props-per-line': ['error', { 'maximum': { 'single': 2, 'multi': 1 } }],
      '@stylistic/jsx-first-prop-new-line': ['error', 'multiline'],
      '@stylistic/jsx-closing-bracket-location': ['error', 'tag-aligned'],

      // --- Next ---
      '@next/next/no-html-link-for-pages': 'error',
    },
    settings: {
      react: { version: 'detect' },
      'import-x/resolver': {
        typescript: {
          alwaysTryTypes: true,
          project: ['./tsconfig.json'],
        },
      },
    },
  },
]);
