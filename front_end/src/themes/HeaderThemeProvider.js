// src/theme/HeaderThemeProvider.js
import React from "react";
import { ThemeProvider as MuiThemeProvider, createTheme } from "@mui/material/styles";
import CssBaseline from "@mui/material/CssBaseline";

// Определение темы для хедера
const headerTheme = createTheme({
    palette: {
        primary: {
            main: "rgba(245, 245, 245, 1)", // светлый цвет фона
        },
        secondary: {
            main: "rgba(44, 44, 44, 1)", // темный цвет текста
        },
        background: {
            default: "rgba(255, 255, 255, 1)", // белый фон
            paper: "rgba(227, 227, 227, 1)", // цвет для внутренних блоков
        },
        text: {
            primary: "rgba(30, 30, 30, 1)", // основной цвет текста
            secondary: "rgba(68, 68, 68, 1)", // дополнительный цвет текста
        },
        divider: "rgba(217, 217, 217, 1)", // цвет разделителей
    },
    typography: {
        fontFamily: "Inter, Helvetica",
        body1: {
            fontSize: "16px",
            fontWeight: 400,
            letterSpacing: "0px",
            lineHeight: "100%",
        },
    },
    components: {
        MuiButton: {
            styleOverrides: {
                root: {
                    textTransform: "none",
                },
            },
        },
    },
});

const HeaderThemeProvider = ({ children }) => {
    return (
        <MuiThemeProvider theme={headerTheme}>
            <CssBaseline />
            {children}
        </MuiThemeProvider>
    );
};

export default HeaderThemeProvider;
