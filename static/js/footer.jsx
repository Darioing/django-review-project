import Instagram from "@mui/icons-material/Instagram";
import LinkedIn from "@mui/icons-material/LinkedIn";
import YouTube from "@mui/icons-material/YouTube";
import { Box, List, ListItem, ListItemText, Typography } from "@mui/material";
import React from "react";

const Footer = () => {
    return (
        <Box
            display="flex"
            flexWrap="wrap"
            width="1920px"
            alignItems="start"
            gap={4}
            pt={8}
            pr={8}
            pb={40}
            pl={8}
            bgcolor="background.default"
            borderTop={1}
            borderColor="divider"
        >
            <Box display="flex" flexDirection="column" alignItems="start" gap={3}>
                <img
                    style={{
                        width: "263.75px",
                        marginTop: "-1.75px",
                        marginLeft: "-1.75px",
                    }}
                    alt="Title"
                    src="title.svg"
                />
                <Box display="flex" gap={1}>
                    <Instagram />
                    <YouTube />
                    <LinkedIn />
                </Box>
            </Box>

            <Box display="flex" flexDirection="column" width="262px" gap={3}>
                <Typography variant="h6" component="div">
                    Use cases
                </Typography>
                <List>
                    {[
                        "UI design",
                        "UX design",
                        "Wireframing",
                        "Diagramming",
                        "Brainstorming",
                        "Online whiteboard",
                        "Team collaboration",
                    ].map((text) => (
                        <ListItem button key={text}>
                            <ListItemText primary={text} />
                        </ListItem>
                    ))}
                </List>
            </Box>

            <Box display="flex" flexDirection="column" width="262px" gap={3}>
                <Typography variant="h6" component="div">
                    Explore
                </Typography>
                <List>
                    {[
                        "Design",
                        "Prototyping",
                        "Development features",
                        "Design systems",
                        "Collaboration features",
                        "Design process",
                        "FigJam",
                    ].map((text) => (
                        <ListItem button key={text}>
                            <ListItemText primary={text} />
                        </ListItem>
                    ))}
                </List>
            </Box>

            <Box display="flex" flexDirection="column" width="262px" gap={3}>
                <Typography variant="h6" component="div">
                    Resources
                </Typography>
                <List>
                    {[
                        "Blog",
                        "Best practices",
                        "Colors",
                        "Color wheel",
                        "Support",
                        "Developers",
                        "Resource library",
                    ].map((text) => (
                        <ListItem button key={text}>
                            <ListItemText primary={text} />
                        </ListItem>
                    ))}
                </List>
            </Box>
        </Box>
    );
};

export default Footer;
