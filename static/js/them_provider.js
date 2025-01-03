import {
    CssBaseline,
    ThemeProvider as MuiThemeProvider,
    createTheme,
} from "@mui/material";
import React from "react";

const appTheme = createTheme({
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
    components: {
        MuiButton: {
            styleOverrides: {
                root: {
                    textTransform: "none",
                },
            },
        },
        MuiTableCell: {
            styleOverrides: {
                root: ({ theme }) => ({
                    ...theme.typography.body1,
                }),
                head: ({ theme }) => ({
                    ...theme.typography.h6,
                }),
                body: ({ theme }) => ({
                    ...theme.typography.body1,
                }),
            },
        },
        MuiListItemText: {
            styleOverrides: {
                primary: ({ theme }) => ({
                    ...theme.typography.body1,
                }),
            },
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
