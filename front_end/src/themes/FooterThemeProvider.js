import {
    CssBaseline,
    ThemeProvider as MuiThemeProvider,
    createTheme,
} from "@mui/material";
import React from "react";

const footerTheme = createTheme({
    palette: {
        background: {
            default: "rgba(255, 255, 255, 1)",
        },
        divider: "rgba(217, 217, 217, 1)",
        text: {
            primary: "rgba(30, 30, 30, 1)",
        },
    },
    typography: {
        fontFamily: "Inter, Helvetica",
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
    },
});

const FooterThemeProvider = ({ children }) => {
    return (
        <MuiThemeProvider theme={footerTheme}>
            <CssBaseline />
            {children}
        </MuiThemeProvider>
    );
};

export default FooterThemeProvider; // Экспортируем по умолчанию
