// src/components/Header.jsx
import React, { useContext } from "react";
import figma from "@mui/icons-material/Star"; // Иконка для логотипа
import { AppBar, Box, Button, Container, Toolbar, Typography } from "@mui/material";
import HeaderThemeProvider from "../themes/HeaderThemeProvider"; // Импортируем ThemeProvider для хедера
import { AuthContext } from "../contexts/AuthContext";

const Header = () => {
    const { isAuthenticated, logout } = useContext(AuthContext);

    return (
        <HeaderThemeProvider>
            <AppBar
                position="static"
                color="default"
                sx={{ borderBottom: 1, borderColor: "divider" }}
            >
                <Container maxWidth="xl">
                    <Toolbar disableGutters>
                        <Box sx={{ display: "flex", alignItems: "center", mr: 2 }}>
                            <img src={figma} alt="Figma" style={{ width: 40 }} />
                        </Box>
                        <Box
                            sx={{
                                flexGrow: 1,
                                display: "flex",
                                justifyContent: "flex-end",
                                gap: 1,
                            }}
                        >
                            {/* Главная страница */}
                            <Button
                                variant="outlined"
                                color="primary"
                                sx={{
                                    borderRadius: 1,
                                    textTransform: "none",
                                    borderColor: "primary.main",
                                    color: "primary.main",
                                    "&:hover": {
                                        borderColor: "primary.dark",
                                        backgroundColor: "primary.light",
                                    },
                                }}
                            >
                                <a href="/" style={{ textDecoration: "none", color: "inherit" }}>
                                    <Typography variant="body1" color="textPrimary">
                                        Главная страница
                                    </Typography>
                                </a>
                            </Button>

                            {/* Поиск */}
                            <Button
                                variant="outlined"
                                color="primary"
                                sx={{
                                    borderRadius: 1,
                                    textTransform: "none",
                                    borderColor: "primary.main",
                                    color: "primary.main",
                                    "&:hover": {
                                        borderColor: "primary.dark",
                                        backgroundColor: "primary.light",
                                    },
                                }}
                            >
                                <a href="/search" style={{ textDecoration: "none", color: "inherit" }}>
                                    <Typography variant="body1" color="textPrimary">
                                        Поиск
                                    </Typography>
                                </a>
                            </Button>

                            {/* Условный рендеринг */}
                            {isAuthenticated ? (
                                <>
                                    {/* Профиль */}
                                    <Button
                                        variant="outlined"
                                        color="primary"
                                        sx={{
                                            borderRadius: 1,
                                            textTransform: "none",
                                            borderColor: "primary.main",
                                            color: "primary.main",
                                            "&:hover": {
                                                borderColor: "primary.dark",
                                                backgroundColor: "primary.light",
                                            },
                                        }}
                                    >
                                        <a
                                            href="/profile"
                                            style={{ textDecoration: "none", color: "inherit" }}
                                        >
                                            <Typography variant="body1" color="textPrimary">
                                                Профиль
                                            </Typography>
                                        </a>
                                    </Button>

                                    {/* Выход */}
                                    <Button
                                        variant="outlined"
                                        color="secondary"
                                        onClick={() => {
                                            logout();
                                            window.location.reload(); // Принудительное обновление страницы
                                        }}
                                        sx={{
                                            borderRadius: 1,
                                            textTransform: "none",
                                            color: "error.main",
                                            "&:hover": {
                                                backgroundColor: "error.light",
                                                borderColor: "error.dark",
                                            },
                                        }}
                                    >
                                        <Typography variant="body1" color="textPrimary">
                                            Выход
                                        </Typography>
                                    </Button>
                                </>
                            ) : (
                                <>
                                    {/* Войти */}
                                    <Button
                                        variant="outlined"
                                        sx={{
                                            borderRadius: 1,
                                            textTransform: "none",
                                            color: "primary.main",
                                            "&:hover": {
                                                backgroundColor: "success.light",
                                                borderColor: "success.dark",
                                            },
                                        }}
                                    >
                                        <a
                                            href="/login"
                                            style={{ textDecoration: "none", color: "inherit" }}
                                        >
                                            <Typography variant="body1" color="textPrimary">
                                                Войти
                                            </Typography>
                                        </a>
                                    </Button>

                                    {/* Регистрация */}
                                    <Button
                                        variant="outlined"
                                        sx={{
                                            borderRadius: 1,
                                            textTransform: "none",
                                            color: "primary.main",
                                            "&:hover": {
                                                backgroundColor: "#FFB841",
                                                borderColor: "success.dark",
                                            },
                                        }}
                                    >
                                        <a
                                            href="/register"
                                            style={{ textDecoration: "none", color: "inherit" }}
                                        >
                                            <Typography variant="body1" color="textPrimary">
                                                Регистрация
                                            </Typography>
                                        </a>
                                    </Button>
                                </>
                            )}
                        </Box>
                    </Toolbar>
                </Container>
            </AppBar>
        </HeaderThemeProvider>
    );
};

export default Header;
