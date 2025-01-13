import React, { useEffect, useState } from "react";
import { Box, IconButton, Typography } from "@mui/material";
import ArrowUpwardIcon from "@mui/icons-material/ArrowUpward";
import ArrowDownwardIcon from "@mui/icons-material/ArrowDownward";

const VoteControl = ({ contentType, objectId, onVote }) => {
    const [votes, setVotes] = useState(0);
    const [userVote, setUserVote] = useState(0); // -1, 0, 1

    useEffect(() => {
        const fetchVotes = async () => {
            try {
                const response = await fetch(
                    `http://127.0.0.1:8000/review/votes/total-votes/?content_type=${contentType}&object_id=${objectId}`
                );
                const data = await response.json();
                setVotes(data.total_votes || 0);

                const userResponse = await fetch(
                    `http://127.0.0.1:8000/review/votes/user-vote/?content_type=${contentType}&object_id=${objectId}`,
                    {
                        headers: {
                            Authorization: `Bearer ${localStorage.getItem("access")}`,
                        },
                    }
                );
                if (userResponse.ok) {
                    const userData = await userResponse.json();
                    setUserVote(userData.user_vote || 0);
                }
            } catch (error) {
                console.error("Ошибка загрузки голосов:", error);
            }
        };

        fetchVotes();
    }, [contentType, objectId]);

    const handleVote = async (voteType) => {
        if (!localStorage.getItem("access")) {
            alert("Необходимо авторизоваться для голосования");
            return;
        }

        const voteData = {
            user_id: localStorage.getItem("user_id"),
            content_type: contentType,
            object_id: objectId,
            vote_type: voteType,
        };

        try {
            const response = await fetch("http://127.0.0.1:8000/review/votes/", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                    Authorization: `Bearer ${localStorage.getItem("access")}`,
                },
                body: JSON.stringify(voteData),
            });

            if (response.ok) {
                const newVote = await response.json();
                setVotes((prev) => prev + voteType - userVote);
                setUserVote(voteType);
                if (onVote) onVote(newVote);
            } else {
                console.error("Ошибка голосования:", await response.text());
            }
        } catch (error) {
            console.error("Ошибка отправки голоса:", error);
        }
    };

    return (
        <Box
            display="flex"
            flexDirection="column" // Вертикальное расположение элементов
            alignItems="center"
        >
            <IconButton
                color={userVote === 1 ? "success" : "default"}
                onClick={() => handleVote(1)}
            >
                <ArrowUpwardIcon
                    style={{
                        fill: userVote === 1 ? "green" : "none",
                        stroke: userVote === 1 ? "green" : "gray",
                        strokeWidth: 2,
                        fontSize: "24px", // Увеличение размера стрелки
                    }}
                />
            </IconButton>
            <Typography variant="body1" sx={{ my: 1 }}> {/* Добавлен вертикальный отступ */}
                {votes}
            </Typography>
            <IconButton
                color={userVote === -1 ? "warning" : "default"}
                onClick={() => handleVote(-1)}
            >
                <ArrowDownwardIcon
                    style={{
                        fill: userVote === -1 ? "orange" : "none",
                        stroke: userVote === -1 ? "orange" : "gray",
                        strokeWidth: 2,
                        fontSize: "24px", // Увеличение размера стрелки
                    }}
                />
            </IconButton>
        </Box>

    );
};

export default VoteControl;
