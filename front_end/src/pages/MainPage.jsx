import React, { useState, useEffect } from "react";
import { Link } from "react-router-dom";
import {
    Box,
    Card,
    CardContent,
    CardMedia,
    Grid,
    Typography,
    Container,
    Rating,
    Button,
    Select,
    MenuItem,
    FormControl,
    InputLabel,
} from "@mui/material";

const MainPage = () => {
    const [places, setPlaces] = useState([]);
    const [visiblePlaces, setVisiblePlaces] = useState(6);
    const [filter, setFilter] = useState("ratingDesc"); // Фильтр по умолчанию

    useEffect(() => {
        fetch("http://127.0.0.1:8000/review/places/")
            .then((response) => response.json())
            .then((data) => {
                setPlaces(sortPlaces(data, filter)); // Сортируем данные при загрузке
            })
            .catch((error) => console.error("Ошибка API:", error));
    }, [filter]);

    const sortPlaces = (placesList, filterType) => {
        switch (filterType) {
            case "ratingDesc":
                return [...placesList].sort((a, b) => (b.rating || 0) - (a.rating || 0));
            case "ratingAsc":
                return [...placesList].sort((a, b) => (a.rating || 0) - (b.rating || 0));
            case "reviewsDesc":
                return [...placesList].sort((a, b) => (b.review_count || 0) - (a.review_count || 0));
            case "reviewsAsc":
                return [...placesList].sort((a, b) => (a.review_count || 0) - (b.review_count || 0));
            default:
                return placesList;
        }
    };

    const handleLoadMore = () => {
        setVisiblePlaces((prev) => prev + 6);
    };

    const handleFilterChange = (event) => {
        setFilter(event.target.value); // Устанавливаем новый фильтр
    };

    const getReviewWord = (count) => {
        const lastDigit = count % 10;
        const lastTwoDigits = count % 100;

        if (lastTwoDigits >= 11 && lastTwoDigits <= 14) {
            return "отзывов";
        }

        if (lastDigit === 1) {
            return "отзыв";
        }

        if (lastDigit >= 2 && lastDigit <= 4) {
            return "отзыва";
        }

        return "отзывов";
    };

    return (
        <Box
            sx={{
                bgcolor: "background.default",
                width: "100%",
                py: 8,
                minHeight: "calc(100vh - 64px - 62px)",
            }}
        >
            <Container maxWidth="xl">
                <Box
                    sx={{
                        display: "flex",
                        flexDirection: "column",
                        alignItems: "start",
                        gap: 1,
                        mb: 2,
                    }}
                >
                    <Typography variant="h4" component="div">
                        Заведения
                    </Typography>
                    <Typography variant="subtitle1" color="text.secondary">
                        Заведения города расположенные по рейтингу
                    </Typography>
                </Box>
                <Box sx={{ display: "flex", justifyContent: "flex-end", mb: 2 }}>
                    <FormControl size="small" sx={{ minWidth: 200, width: "300px" }}>
                        <InputLabel>Фильтрация</InputLabel>
                        <Select
                            value={filter}
                            onChange={handleFilterChange}
                            label="Фильтрация"
                        >
                            <MenuItem value="ratingDesc">Рейтинг: от высокого к низкому</MenuItem>
                            <MenuItem value="reviewsDesc">Отзывы: от большего к меньшему</MenuItem>
                        </Select>
                    </FormControl>
                </Box>
                <Grid container spacing={6} sx={{ mt: 4 }}>
                    {places.slice(0, visiblePlaces).map((place) => (
                        <Grid item xs={12} sm={6} md={4} key={place.id}>
                            <Card
                                component={Link}
                                to={`/place/${place.slug}`}
                                sx={{
                                    display: "flex",
                                    flexDirection: "column",
                                    alignItems: "start",
                                    gap: 3,
                                    p: 3,
                                    bgcolor: "background.default",
                                    borderRadius: 1,
                                    border: 1,
                                    borderColor: "divider",
                                    height: 400,
                                    textDecoration: "none"
                                }}
                            >
                                <CardMedia
                                    component="img"
                                    image={place.photos[0] || "/default-image.jpg"}
                                    alt={place.name}
                                    sx={{
                                        width: "100%",
                                        height: 160,
                                        backgroundSize: "cover",
                                        backgroundPosition: "center",
                                    }}
                                />
                                <CardContent
                                    sx={{
                                        display: "flex",
                                        flexDirection: "column",
                                        gap: 2,
                                        width: "100%",
                                        flexGrow: 1,
                                    }}
                                >
                                    <Typography
                                        component="div"
                                        variant="h6"
                                    >
                                        {place.name}
                                    </Typography>
                                    <Box
                                        sx={{
                                            display: "flex",
                                            alignItems: "center",
                                            gap: 1,
                                        }}
                                    >
                                        <Rating
                                            value={place.rating || 0}
                                            precision={0.1}
                                            readOnly
                                        />
                                        <Typography
                                            variant="body2"
                                            color="text.secondary"
                                        >
                                            {place.rating
                                                ? `${place.rating.toFixed(2)}`
                                                : "Нет рейтинга"}
                                        </Typography>
                                        {place.review_count > 0 && (
                                            <Typography
                                                variant="body2"
                                                color="text.secondary"
                                            >
                                                ({place.review_count} {getReviewWord(place.review_count)})
                                            </Typography>
                                        )}
                                    </Box>
                                    <Typography
                                        variant="body1"
                                        color="text.secondary"
                                        sx={{
                                            overflow: "hidden",
                                            textOverflow: "ellipsis",
                                            display: "-webkit-box",
                                            WebkitBoxOrient: "vertical",
                                            WebkitLineClamp: 3,
                                            maxHeight: "4.5em",
                                        }}
                                    >
                                        {place.about}
                                    </Typography>
                                </CardContent>
                            </Card>
                        </Grid>
                    ))}
                </Grid>
                {visiblePlaces < places.length && (
                    <Box sx={{ display: "flex", justifyContent: "center", mt: 4 }}>
                        <Button
                            variant="contained"
                            color="primary"
                            onClick={handleLoadMore}
                        >
                            Еще
                        </Button>
                    </Box>
                )}
            </Container>
        </Box>
    );
};

export default MainPage;
