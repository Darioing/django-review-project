import ExpandMore from "@mui/icons-material/ExpandMore";
import Favorite from "@mui/icons-material/Favorite";
import Star from "@mui/icons-material/Star";
import ArrowBackIosIcon from "@mui/icons-material/ArrowBackIos";
import ArrowForwardIosIcon from "@mui/icons-material/ArrowForwardIos";
import {
    Box,
    Button,
    Container,
    IconButton,
    Typography,
} from "@mui/material";
import React, { useEffect, useState } from "react";
import { useParams, useNavigate } from "react-router-dom"; // Добавлен useNavigate
import ReviewsByPlace from "../components/ReviewsByPlace";
import QuestionsByPlace from "../components/QuestionsByPlace"; // Новый компонент для вопросов

const PlaceDetails = () => {
    const { slug } = useParams(); // Получение slug из параметров маршрута
    const [place, setPlace] = useState(null);
    const [currentImageIndex, setCurrentImageIndex] = useState(0);
    const [view, setView] = useState("reviews"); // Состояние переключателя: "reviews" или "questions"
    const navigate = useNavigate(); // Для перенаправления

    useEffect(() => {
        // Запрос к API для получения данных заведения
        fetch(`http://127.0.0.1:8000/review/places/${slug}/`)
            .then((response) => {
                if (!response.ok) {
                    throw new Error("Ошибка при загрузке данных заведения");
                }
                return response.json();
            })
            .then((data) => {
                setPlace(data);
                setCurrentImageIndex(0); // Сброс индекса при загрузке новых данных
            })
            .catch((error) => console.error("Ошибка:", error));
    }, [slug]);

    const handlePrevImage = () => {
        if (place.photos && place.photos.length > 0) {
            setCurrentImageIndex((prevIndex) =>
                prevIndex === 0 ? place.photos.length - 1 : prevIndex - 1
            );
        }
    };

    const handleNextImage = () => {
        if (place.photos && place.photos.length > 0) {
            setCurrentImageIndex((prevIndex) =>
                prevIndex === place.photos.length - 1 ? 0 : prevIndex + 1
            );
        }
    };

    const isUserAuthenticated = !!localStorage.getItem("access"); // Проверка на авторизацию

    if (!place) {
        return (
            <Box
                display="flex"
                justifyContent="center"
                alignItems="center"
                minHeight="calc(100vh - 64px - 62px)"
            >
                <Typography variant="h6">Загрузка данных...</Typography>
            </Box>
        );
    }

    return (
        <Box
            display="flex"
            flexDirection="column"
            alignItems="flex-start"
            bgcolor="background.default"
            width="100%"
            sx={{
                bgcolor: "background.default",
                width: "100%",
                py: 4,
                minHeight: "calc(100vh - 64px - 62px)",
            }}
        >
            <Container maxWidth="xl">
                {/* Информация о заведении */}
                <Box
                    display="flex"
                    flexDirection="column"
                    gap={6}
                    p={4}
                    width="100%"
                >
                    <Box display="flex" gap={6} width="100%">
                        {/* Галерея изображений */}
                        <Box
                            flex={1}
                            height={300}
                            bgcolor="grey.300"
                            display="flex"
                            justifyContent="center"
                            alignItems="center"
                            position="relative"
                        >
                            <IconButton
                                sx={{
                                    position: "absolute",
                                    top: 10,
                                    left: 10,
                                    bgcolor: "primary.main",
                                    color: "primary.contrastText",
                                    "&:hover": {
                                        bgcolor: "primary.dark",
                                    },
                                }}
                            >
                                <Favorite />
                            </IconButton>
                            <IconButton
                                onClick={handlePrevImage}
                                sx={{
                                    position: "absolute",
                                    left: 10,
                                    top: "50%",
                                    transform: "translateY(-50%)",
                                    bgcolor: "primary.main",
                                    color: "primary.contrastText",
                                    "&:hover": {
                                        bgcolor: "primary.dark",
                                    },
                                }}
                            >
                                <ArrowBackIosIcon />
                            </IconButton>
                            {place.photos && place.photos.length > 0 && (
                                <img
                                    src={place.photos[currentImageIndex]}
                                    alt={`${place.name} - ${currentImageIndex + 1}`}
                                    style={{
                                        width: "100%",
                                        height: "100%",
                                        objectFit: "cover",
                                    }}
                                />
                            )}
                            <IconButton
                                onClick={handleNextImage}
                                sx={{
                                    position: "absolute",
                                    right: 10,
                                    top: "50%",
                                    transform: "translateY(-50%)",
                                    bgcolor: "primary.main",
                                    color: "primary.contrastText",
                                    "&:hover": {
                                        bgcolor: "primary.dark",
                                    },
                                }}
                            >
                                <ArrowForwardIosIcon />
                            </IconButton>
                        </Box>

                        {/* Основная информация */}
                        <Box flex={1} display="flex" flexDirection="column" gap={2}>
                            <Box display="flex" flexDirection="column" gap={1}>
                                <Typography variant="h5">{place.name}</Typography>
                                <Box
                                    display="inline-flex"
                                    alignItems="center"
                                    gap={1}
                                    p={1}
                                    bgcolor="success.light"
                                    borderRadius={1}
                                    sx={{ width: "fit-content" }}
                                >
                                    <Typography
                                        variant="tag"
                                        color="success.contrastText"
                                        sx={{ display: "inline" }}
                                    >
                                        {place.category_name || "Категория отсутствует"}
                                    </Typography>
                                </Box>
                                <Box display="flex" alignItems="center" gap={1}>
                                    <Star color="warning" />
                                    <Typography variant="body1">
                                        {place.rating ? place.rating.toFixed(2) : "Нет рейтинга"}
                                    </Typography>
                                </Box>
                            </Box>
                            <Typography variant="body2" color="textSecondary">
                                {place.address}
                            </Typography>
                            <Typography variant="body2" color="textSecondary">
                                {place.about}
                            </Typography>
                            {/* Кнопка для добавления отзыва */}
                            {isUserAuthenticated && (
                                <Box display="flex" justifyContent="center" my={3} gap={2}>
                                    <Button
                                        variant="outlined"
                                        color="primary.main"
                                        sx={{
                                            borderRadius: 1,
                                            textTransform: "none",
                                            borderColor: "rgba(179, 179, 179, 1)",
                                            "&:hover": {
                                                borderColor: "primary.main",
                                                backgroundColor: "rgba(245, 245, 245, 1)",
                                            },
                                        }}
                                        onClick={() => navigate(`/add-review/${place.slug}`)}
                                    >
                                        Оставить отзыв
                                    </Button>
                                    <Button
                                        variant="outlined"
                                        color="primary.main"
                                        sx={{
                                            borderRadius: 1,
                                            textTransform: "none",
                                            borderColor: "rgba(179, 179, 179, 1)",
                                            "&:hover": {
                                                borderColor: "primary.main",
                                                backgroundColor: "rgba(245, 245, 245, 1)",
                                            },
                                        }}
                                        onClick={() => navigate(`/add-question/${slug}`)}
                                    >
                                        Задать вопрос
                                    </Button>
                                </Box>
                            )}
                        </Box>
                    </Box>
                </Box>



                {/* Переключатель между отзывами и вопросами */}
                <Box display="flex" justifyContent="center" gap={2} my={3}>
                    <Button
                        variant={view === "reviews" ? "contained" : "outlined"}
                        onClick={() => setView("reviews")}
                    >
                        Отзывы
                    </Button>
                    <Button
                        variant={view === "questions" ? "contained" : "outlined"}
                        onClick={() => setView("questions")}
                    >
                        Вопросы
                    </Button>
                </Box>

                {/* Контент в зависимости от выбора */}
                {view === "reviews" ? (
                    <ReviewsByPlace placeId={place.id} />
                ) : (
                    <QuestionsByPlace placeId={place.id} />
                )}
            </Container>
        </Box>
    );
};

export default PlaceDetails;
