import js from "@eslint/js";
import { FlatCompat } from "@eslint/eslintrc";

const compat = new FlatCompat({
  baseDirectory: import.meta.dirname,
  recommendedConfig: js.configs.recommended,
});

const eslintConfig = [
  ...compat.config({
    ignorePatterns: [
      "eslint.config.mjs",
      "node_modules",
      ".prettierrc",
      "package.json",
      "tailwind.config.ts",
    ],
    extends: [
      "eslint:recommended",
      "next",
      "next/core-web-vitals",
      "airbnb",
      "airbnb/hooks",
      "plugin:import/recommended",
      "plugin:jsx-a11y/recommended",
    ],
    plugins: ["import", "jsx-a11y", "react", "@typescript-eslint"],
    rules: {
      // console 은 log 는 경고, warn 과 error 는 로직상 필요함으로 무시
      "no-console": ["warn", { allow: ["warn", "error"] }],
      // 들여쓰기 2칸
      "indent": ["error", "2tab", { SwitchCase: 1 }],
      // double quotes 사용
      "quotes": ["error", "double", { avoidEscape: true }],
      // double quotes 사용 (ts용)
      "@/quotes": ["error", "double"],
      // endOfLine 맥을 사용하기에 \n (o) \r\n (x),
      "linebreak-style": "off",
      // 사용안한 변수 경고 x
      "no-unused-vars": "off",
      // 사용안한 변수는 경고 (ts용) - 겹치기 때문에 ts 용만 경고로 한다.
      "@typescript-eslint/no-unused-vars": "warn",
      // js, jsx, tsx 확장자만 허가
      "react/jsx-filename-extension": [1, { extensions: [".js", ".jsx", ".tsx"] }],
      // import 파일 확장자 생략
      "import/extensions": [
        "error",
        // 라이브러리 import 확장자도 생략
        "ignorePackages",
        {
          js: "never",
          jsx: "never",
          ts: "never",
          tsx: "never",
        },
      ],
      // import 우선순위 정렬
      "import/order": [
        "error",
        {
          groups: ["builtin", "external", "internal", "type"],
        },
      ],
      // 2줄 이상 빈줄 에러
      "no-multiple-empty-lines": ["error", { max: 2, maxBOF: 1 }],
      // const function 허용
      "react/function-component-definition": "off",
      // 화살표 함수 안에 return 사용 활성화
      "arrow-body-style": "off",
      // <label> <input> 에서 htmlFor 와 input id의 필수값을 제거
      "jsx-a11y/label-has-associated-control": "off",
      // 상호작용하는 엘리먼트에 label 안 써도 되게
      "jsx-a11y/control-has-associated-label": "off",
      // 마지막에 , 을 넣어준다.
      "comma-dangle": 1,
      // 직관성에 영향을 주는 의미 있는 줄바꿈은 권장한다.
      "no-trailing-spaces": "off",
      // 상황에 따라 한 줄, 여러 줄을 선택한다.
      "object-curly-newline": "off",
      // operator 가 포함 된 멀티 라인 대응
      "operator-linebreak": "off",
      // jsx 한 줄에 여러번 쓸 수 있게
      "react/jsx-one-expression-per-line": "off",
      // import React from react 안 써도 되게
      "react/react-in-jsx-scope": "off",
      // export default 를 우선 시 하는 규칙
      "import/prefer-default-export": "off",
      // 상황에 따라 arrow function 은 줄을 바꿀 수 있게 한다.
      "implicit-arrow-linebreak": "off",
      // 정의 되기 전에 사용 허가 (같은 파일 안에서만 사용하기)
      "no-use-before-define": "off",
      // props 에 관련해서는 구조분해를 사용하지 않는다.
      "react/destructuring-assignment": "off",
      // 첫 글자를 _로 시작할 수 있게 한다.
      "no-underscore-dangle": "off",
      // undefined 를 명시적으로 리턴해주기 위해서
      "consistent-return": "off",
      // 파일 내 중복 이름 가능
      "no-shadow": "off",
      // 지역적 require 활성화
      "global-require": "off",
      // default-props 필수 제거
      "react/require-default-props": "off",
      // alert 허용
      "no-alert": "off",
      // 객체 [" "] 접근 허용
      "dot-notation": "off",
      // 파일 당 max classes 횟수 제한 x
      "max-classes-per-file": "off",
      // class methods에서 this 사용 강제 x
      "class-methods-use-this": "off",
      // global 변수 (window, location) 참조 허용
      "no-restricted-globals": "off",
      // 파라미터 무조건 줄바꿈 비활성화
      "function-paren-newline": "off",
      // static-element에 event 달 수 있게
      "jsx-a11y/no-static-element-interactions": "off",
      // no-noninteractive-element에 event 달 수 있게
      "jsx-a11y/no-noninteractive-element-interactions": "off",
      // 클릭 이벤트에 대한 키보드 이벤트 필수 제거
      "jsx-a11y/click-events-have-key-events": "off",
      // class 에서 변수 줄바꿈 필수 예외
      "lines-between-class-members": "off",
      // req {} 사용을 위해
      "no-empty-pattern": "off",
      // 상황에 따라 다르지만 @ path 를 사용하기 위해 비활성화
      "import/no-unresolved": "off",
      // arrow function에서 할당 반환 가능하게
      "no-return-assign": "off",
      // mobx model의 직접 할당을 위해
      "no-param-reassign": "off",
      // a++, a-- 가능하게 변경 (요청 사항)
      "no-plusplus": "off",
      // 19자 이후 >(closing-tag) 허용......
      "react/jsx-closing-bracket-location": "off",
      // <></> 사용 가능
      "react/jsx-no-useless-fragment": "off",
      // 배열 구조분해 할당 필수 제거
      "prefer-destructuring": "off",
      // if문에서 크기 비교는 항상 > 으로 하기로 한다.
      "yoda": "off",
      // function 앞에서 공간 넣기 O
      "space-before-function-paren": "off",
      // jsx 안에서 중괄호 줄바꿈 서용
      "react/jsx-curly-newline": "off",
      // 직접 import 방지 비활성화
      "import/no-import-module-exports": "off",
      // deps 외에 다른 모듈 import 방지 비활성화
      "import/no-extraneous-dependencies": "off",
      // loop continue 사용 허용
      "no-continue": "off",
      // 자동 완성되는 interface 는 빈 interface 가 될수 있기에 비활성화
      "@typescript-eslint/no-empty-object-type": "off",
      // faker 에서 loop 안에 await 사용을 위해
      "no-await-in-loop": "off",
      // javaScript 기능이나 구문을 사용
      "no-restricted-syntax": "off",
    },
  }),
];

export default eslintConfig;
