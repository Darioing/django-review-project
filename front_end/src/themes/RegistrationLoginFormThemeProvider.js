import {
    CssBaseline,
    ThemeProvider as MuiThemeProvider,
    createTheme,
} from "@mui/material";
import React from "react";

const appTheme = createTheme({
    palette: {
        primary: {
            main: "rgba(44, 44, 44, 1)",
        },
        secondary: {
            main: "rgba(117, 117, 117, 1)",
        },
        error: {
            main: "rgba(220, 27, 36, 1)",
        },
        background: {
            default: "rgba(255, 255, 255, 1)",
        },
        text: {
            primary: "rgba(30, 30, 30, 1)",
            secondary: "rgba(117, 117, 117, 1)",
            disabled: "rgba(179, 179, 179, 1)",
        },
        border: {
            default: "rgba(217, 217, 217, 1)",
        },
    },
    typography: {
        fontFamily: "Inter, Helvetica",
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
    },
});

export const ThemeProvider = ({ children }) => {
    return (
        <MuiThemeProvider theme={appTheme}>
            <CssBaseline />
            {children}
        </MuiThemeProvider>
    );
};

