// src/themes/GlobalThemeProvider.js
import React from "react";
import {
    CssBaseline,
    ThemeProvider as MuiThemeProvider,
    createTheme,
} from "@mui/material";

// Объединённая тема
const globalTheme = createTheme({
    palette: {
        primary: {
            main: "rgba(44, 44, 44, 1)", // Общий цвет кнопок и других элементов
        },
        secondary: {
            main: "rgba(117, 117, 117, 1)", // Общий цвет текста или акцентов
        },
        error: {
            main: "rgba(220, 27, 36, 1)", // Цвет ошибок
        },
        background: {
            default: "rgba(255, 255, 255, 1)", // Фон приложения
        },
        text: {
            primary: "rgba(30, 30, 30, 1)", // Основной текст
            secondary: "rgba(117, 117, 117, 1)", // Второстепенный текст
            disabled: "rgba(179, 179, 179, 1)", // Отключённый текст
        },
        divider: "rgba(217, 217, 217, 1)", // Цвет разделителей
        border: {
            default: "rgba(217, 217, 217, 1)", // Цвет рамок
        },
    },
    typography: {
        fontFamily: "Inter, Helvetica", // Общий шрифт
        h4: {
            fontSize: "24px",
            fontWeight: 600,
            letterSpacing: "-0.48px",
            lineHeight: "120%",
        },
        subtitle1: {
            fontSize: "20px",
            fontWeight: 400,
            lineHeight: "120%",
        },
        h6: {
            fontSize: "16px",
            fontWeight: 600,
            lineHeight: "140%",
        },
        body1: {
            fontSize: "16px",
            fontWeight: 400,
            lineHeight: "140%",
        },
        body2: {
            fontSize: "16px",
            fontWeight: 400,
            lineHeight: "100%",
        },
        tag: {
            fontSize: "16px",
            fontWeight: 400,
            letterSpacing: "0px",
        }
    },
    components: {
        MuiButton: {
            styleOverrides: {
                root: {
                    textTransform: "none", // Убираем заглавные буквы в кнопках
                },
            },
        },
        MuiTableCell: {
            styleOverrides: {
                root: ({ theme }) => ({
                    ...theme.typography.body1,
                }),
                head: ({ theme }) => ({
                    ...theme.typography.subtitle1,
                }),
                body: ({ theme }) => ({
                    ...theme.typography.body1,
                }),
            },
        },
        MuiListItemText: {
            styleOverrides: {
                primary: ({ theme }) => ({
                    ...theme.typography.h6,
                }),
                secondary: ({ theme }) => ({
                    ...theme.typography.body1,
                }),
            },
        },
    },
});

// Глобальный ThemeProvider
const GlobalThemeProvider = ({ children }) => {
    return (
        <MuiThemeProvider theme={globalTheme}>
            <CssBaseline />
            {children}
        </MuiThemeProvider>
    );
};

export default GlobalThemeProvider;
