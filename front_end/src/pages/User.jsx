import React, { useEffect, useState } from "react";
import { Box, Button, Container, Typography, Avatar, TextField, IconButton } from "@mui/material";
import { useNavigate } from "react-router-dom";
import EditIcon from "@mui/icons-material/Edit";

const UserProfile = () => {
    const navigate = useNavigate();
    const [user, setUser] = useState(null); // Состояние для данных пользователя
    const [editMode, setEditMode] = useState(false); // Состояние для режима редактирования
    const [fio, setFio] = useState("");
    const [avatar, setAvatar] = useState(null); // Новый аватар пользователя

    useEffect(() => {
        // Запрос данных пользователя (авторизованного)
        fetch("http://127.0.0.1:8000/user/profiles/me/", {
            headers: {
                Authorization: `Bearer ${localStorage.getItem("access")}`,
            },
        })
            .then((response) => response.json())
            .then((data) => {
                setUser(data);
                setFio(data.FIO);
            })
            .catch((error) => console.error("Ошибка:", error));
    }, []);

    const handleSave = () => {
        // Обновление данных пользователя
        const formData = new FormData();
        formData.append("FIO", fio);
        if (avatar) formData.append("image", avatar);

        fetch("http://127.0.0.1:8000/user/profiles/me/", {
            method: "PATCH",
            headers: {
                Authorization: `Bearer ${localStorage.getItem("access")}`,
            },
            body: formData,
        })
            .then((response) => {
                if (!response.ok) throw new Error("Ошибка при сохранении профиля");
                return response.json();
            })
            .then((data) => {
                setUser(data);
                setEditMode(false); // Выход из режима редактирования
            })
            .catch((error) => console.error("Ошибка:", error));
    };

    if (!user) {
        return (
            <Box
                sx={{
                    display: "flex",
                    justifyContent: "center",
                    alignItems: "center",
                    minHeight: "calc(100vh - 64px - 62px)",
                    backgroundColor: "background.default",
                }}
            >
                <Typography variant="h6">Загрузка профиля...</Typography>
            </Box>
        );
    }

    return (
        <Box
            sx={{
                display: "flex",
                flexDirection: "column",
                justifyContent: "center",
                alignItems: "center",
                minHeight: "calc(100vh - 64px - 62px)", // Учитывается высота шапки и футера
                backgroundColor: "background.default",
                padding: "16px",
            }}
        >
            {/* Карточка профиля */}
            <Container
                maxWidth="sm"
                sx={{
                    padding: "24px",
                    backgroundColor: "background.paper",
                    borderRadius: "8px",
                    boxShadow: "0 4px 10px rgba(0, 0, 0, 0.1)",
                    display: "flex",
                    flexDirection: "column",
                    alignItems: "center",
                }}
            >
                {/* Заголовок */}
                <Typography variant="h4" gutterBottom>
                    Профиль пользователя
                </Typography>

                {/* Аватар */}
                <Avatar
                    src={avatar ? URL.createObjectURL(avatar) : user.image}
                    alt={user.FIO}
                    sx={{ width: 120, height: 120, marginBottom: "16px", border: "2px solid #ccc" }}
                />
                {editMode && (
                    <Button
                        variant="contained"
                        component="label"
                        sx={{ marginBottom: "16px" }}
                    >
                        Загрузить аватар
                        <input
                            type="file"
                            accept="image/*"
                            hidden
                            onChange={(e) => {
                                const file = e.target.files[0];
                                if (file) setAvatar(file);
                            }}
                        />
                    </Button>
                )}

                {/* Поле для имени */}
                <Typography variant="h6" gutterBottom>
                    Имя
                </Typography>
                {editMode ? (
                    <TextField
                        value={fio}
                        onChange={(e) => setFio(e.target.value)}
                        fullWidth
                        variant="outlined"
                        sx={{ marginBottom: "16px" }}
                    />
                ) : (
                    <Typography variant="body1" gutterBottom>
                        {user.FIO}
                    </Typography>
                )}

                {/* Кнопки */}
                {editMode ? (
                    <Box display="flex" gap={2} mt={2}>
                        <Button variant="contained" color="primary" onClick={handleSave}>
                            Сохранить
                        </Button>
                        <Button
                            variant="outlined"
                            color="secondary"
                            onClick={() => {
                                setEditMode(false);
                                setAvatar(null); // Отменить локальные изменения аватара
                            }}
                        >
                            Отмена
                        </Button>
                    </Box>
                ) : (
                    <Button
                        variant="contained"
                        startIcon={<EditIcon />}
                        onClick={() => setEditMode(true)}
                        sx={{ marginTop: "16px" }}
                    >
                        Редактировать
                    </Button>
                )}
            </Container>
        </Box>
    );
};

export default UserProfile;