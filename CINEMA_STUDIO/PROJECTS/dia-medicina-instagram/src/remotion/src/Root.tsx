import React from "react";
import {Composition} from "remotion";
import {Type} from "./Type";

export const Root: React.FC = () => (
	<Composition id="Type" component={Type} durationInFrames={720} fps={24} width={1920} height={1080} />
);
