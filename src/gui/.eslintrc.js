module.exports = {
    env: {
        browser: true,
        es2021: true
    },
    extends: [
        'plugin:react/recommended',
        'standard'
    ],
    overrides: [],
    parserOptions: {
        ecmaVersion: 'latest',
        sourceType: 'module'
    },
    plugins: [
        'react'
    ],
    rules: {
        'react/react-in-jsx-scope': 'off',
        'no-unused-vars': 'off',
        'react/prop-types': 'off',
        "semi": ["error", "always", {"omitLastInOneLineBlock": false}],
        "semi-style": ["error", "last"],
        "no-extra-semi": ["error"],
        "semi-spacing": ["error", {"before": false, "after": true}]
    }
}
