import React, { useState } from "react";
import {
    Box,
    IconButton,
    TextField,
    List,
    ListItemButton,
    ListItemText,
    Typography,
} from "@mui/material";
import CloseIcon from "@mui/icons-material/Close";

const Search = () => {
    const [value, setValue] = useState("");
    const [results, setResults] = useState([]);
    const [isSearching, setIsSearching] = useState(false);
    const [searchPerformed, setSearchPerformed] = useState(false); // Флаг, указывающий, был ли выполнен поиск

    const fetchPlaces = async (query) => {
        try {
            const response = await fetch(
                `http://127.0.0.1:8000/review/places/?name=${encodeURIComponent(query)}`
            );
            if (response.ok) {
                const data = await response.json();
                setResults(data);
            } else {
                console.error("Ошибка при загрузке данных:", await response.text());
                setResults([]);
            }
        } catch (error) {
            console.error("Ошибка запроса:", error);
            setResults([]);
        } finally {
            setIsSearching(false);
            setSearchPerformed(true); // Устанавливаем флаг после завершения поиска
        }
    };

    const handleKeyDown = (e) => {
        if (e.key === "Enter" && value.trim()) {
            setIsSearching(true);
            setSearchPerformed(false); // Сбрасываем флаг перед новым поиском
            fetchPlaces(value.trim());
        }
    };

    const handleChange = (e) => {
        setValue(e.target.value);
        setResults([]);
        setSearchPerformed(false); // Сбрасываем флаг при изменении ввода
    };

    const handleClear = () => {
        setValue("");
        setResults([]);
        setSearchPerformed(false); // Сбрасываем флаг при очистке
    };

    return (
        <Box
            position="relative"
            display="flex"
            flexDirection="column"
            alignItems="flex-start"
            gap={1}
            bgcolor="background.default"
            width={300}
        >
            <Box
                display="flex"
                alignItems="center"
                gap={2}
                bgcolor="background.default"
                borderRadius={1}
                border={1}
                borderColor="divider"
                width="100%"
            >
                <TextField
                    value={value}
                    onChange={handleChange}
                    onKeyDown={handleKeyDown}
                    placeholder="Поиск по названию заведения"
                    variant="standard"
                    fullWidth
                    InputProps={{
                        disableUnderline: true,
                        sx: {
                            paddingLeft: 1,
                        },
                    }}
                />
                {value && (
                    <IconButton size="small" onClick={handleClear}>
                        <CloseIcon />
                    </IconButton>
                )}
            </Box>
            {isSearching && (
                <Typography
                    sx={{
                        position: "absolute",
                        top: "calc(100% + 8px)",
                        left: 0,
                        width: "100%",
                        bgcolor: "background.paper",
                        boxShadow: "0px 4px 10px rgba(0,0,0,0.1)",
                        borderRadius: 1,
                        zIndex: 10,
                        p: 1,
                        textAlign: "center",
                    }}
                    variant="body2"
                    color="text.secondary"
                >
                    Поиск...
                </Typography>
            )}
            {results.length > 0 && (
                <List
                    sx={{
                        position: "absolute",
                        top: "calc(100% + 8px)",
                        left: 0,
                        width: "100%",
                        bgcolor: "background.paper",
                        boxShadow: "0px 4px 10px rgba(0,0,0,0.1)",
                        borderRadius: 1,
                        zIndex: 10,
                    }}
                >
                    {results.map((place) => (
                        <ListItemButton
                            key={place.id}
                            onClick={() => {
                                window.location.href = `/place/${place.slug}`;
                            }}
                        >
                            <ListItemText primary={place.name} />
                        </ListItemButton>
                    ))}
                </List>
            )}
            {!isSearching && searchPerformed && results.length === 0 && (
                <Typography
                    sx={{
                        position: "absolute",
                        top: "calc(100% + 8px)",
                        left: 0,
                        width: "100%",
                        bgcolor: "background.paper",
                        boxShadow: "0px 4px 10px rgba(0,0,0,0.1)",
                        borderRadius: 1,
                        zIndex: 10,
                        p: 1,
                        textAlign: "center",
                    }}
                    variant="body2"
                    color="text.secondary"
                >
                    Ничего не найдено
                </Typography>
            )}
        </Box>
    );
};

export default Search;
