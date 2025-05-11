import React, { useState, useContext } from "react";
import axios from "axios";
import {
    Box,
    Button,
    Checkbox,
    Dialog,
    DialogActions,
    DialogContent,
    DialogTitle,
    FormControlLabel,
    TextField,
    Typography,
    Link
} from "@mui/material";
import CheckIcon from "@mui/icons-material/Check";
import { AuthContext } from "../contexts/AuthContext";
import { setTokens } from "../utils/auth";
import { useNavigate } from "react-router-dom";

const FormRegister = () => {
    const [FIO, setFIO] = useState("");
    const [email, setEmail] = useState("");
    const [password, setPassword] = useState("");
    const [agreement, setAgreement] = useState(false);
    const [showSuccessDialog, setShowSuccessDialog] = useState(false);
    const [verificationLink, setVerificationLink] = useState("");
    const { setIsAuthenticated } = useContext(AuthContext);
    const navigate = useNavigate();

    const handleRegister = async () => {
        try {
            if (!agreement) {
                alert("Вы должны согласиться с условиями!");
                return;
            }

            // 1. Отправка данных регистрации
            const response = await axios.post(
                "http://127.0.0.1:8000/user/register/",
                { FIO, email, password },
                {
                    headers: {
                        "Content-Type": "application/json"
                    }
                }
            );

            // 2. Показываем ссылку для тестирования
            setVerificationLink(response.data.test_link || "Ссылка сохранена в файл");
            setShowSuccessDialog(true);

        } catch (error) {
            console.error("Ошибка регистрации:", error.response?.data);
            alert(error.response?.data?.error || "Ошибка регистрации");
        }
    };

    return (
        <Box
            sx={{
                display: "flex",
                justifyContent: "center",
                alignItems: "center",
                minHeight: "calc(100vh - 64px - 62px)",
                backgroundColor: "background.default",
                padding: "16px",
            }}
        >
            {/* Основная форма регистрации */}
            <Box
                sx={{
                    width: "100%",
                    maxWidth: "400px",
                    padding: "24px",
                    backgroundColor: "background.paper",
                    borderRadius: "8px",
                    boxShadow: "0 4px 10px rgba(0, 0, 0, 0.1)",
                    display: "flex",
                    flexDirection: "column",
                    alignItems: "center",
                }}
            >
                <Typography variant="h5" align="center" gutterBottom>
                    Регистрация
                </Typography>

                <TextField
                    fullWidth
                    label="ФИО"
                    value={FIO}
                    onChange={(e) => setFIO(e.target.value)}
                    sx={{ marginBottom: "16px" }}
                />
                <TextField
                    fullWidth
                    label="Email"
                    type="email"
                    value={email}
                    onChange={(e) => setEmail(e.target.value)}
                    sx={{ marginBottom: "16px" }}
                />
                <TextField
                    fullWidth
                    label="Пароль"
                    type="password"
                    value={password}
                    onChange={(e) => setPassword(e.target.value)}
                    sx={{ marginBottom: "16px" }}
                />

                <FormControlLabel
                    control={
                        <Checkbox
                            checked={agreement}
                            onChange={(e) => setAgreement(e.target.checked)}
                            icon={
                                <Box
                                    sx={{
                                        width: "24px",
                                        height: "24px",
                                        border: "2px solid black",
                                        display: "flex",
                                        alignItems: "center",
                                        justifyContent: "center",
                                    }}
                                >
                                    <CheckIcon sx={{ color: "black", fontSize: "16px" }} />
                                </Box>
                            }
                            checkedIcon={
                                <Box
                                    sx={{
                                        width: "24px",
                                        height: "24px",
                                        border: "2px solid black",
                                        backgroundColor: "lightgreen",
                                        display: "flex",
                                        alignItems: "center",
                                        justifyContent: "center",
                                    }}
                                >
                                    <CheckIcon sx={{ color: "black", fontSize: "16px" }} />
                                </Box>
                            }
                        />
                    }
                    label="Я соглашаюсь на обработку пользовательских данных"
                    sx={{ marginBottom: "16px" }}
                />

                <Button
                    fullWidth
                    variant="contained"
                    onClick={handleRegister}
                    sx={{ marginTop: "8px" }}
                >
                    Зарегистрироваться
                </Button>
            </Box>

            {/* Модальное окно с ссылкой для подтверждения */}
            <Dialog open={showSuccessDialog} onClose={() => setShowSuccessDialog(false)}>
                <DialogTitle>Регистрация почти завершена</DialogTitle>
                <DialogContent>
                    <Typography sx={{ mb: 2 }}>
                        Для завершения регистрации перейдите по ссылке из отправленного вам письма:
                    </Typography>
                </DialogContent>
                <DialogActions>
                    <Button onClick={() => setShowSuccessDialog(false)}>Закрыть</Button>
                </DialogActions>
            </Dialog>
        </Box>
    );
};

export default FormRegister;