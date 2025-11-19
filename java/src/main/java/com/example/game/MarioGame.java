package com.example.game;

import com.almasb.fxgl.app.GameApplication;
import com.almasb.fxgl.app.GameSettings;
import com.almasb.fxgl.app.scene.Viewport;
import com.almasb.fxgl.dsl.FXGL;
import com.almasb.fxgl.entity.Entity;
import com.almasb.fxgl.entity.EntityFactory;
import com.almasb.fxgl.entity.SpawnData;
import com.almasb.fxgl.entity.Spawns;
import com.almasb.fxgl.entity.components.CollidableComponent;
import com.almasb.fxgl.entity.components.IrremovableComponent;
import com.almasb.fxgl.input.UserAction;
import com.almasb.fxgl.physics.BoundingShape;
import com.almasb.fxgl.physics.HitBox;
import com.almasb.fxgl.physics.PhysicsComponent;
import com.almasb.fxgl.physics.box2d.dynamics.BodyType;
import com.almasb.fxgl.physics.box2d.dynamics.FixtureDef;
import com.almasb.fxgl.texture.Texture;
import javafx.geometry.Point2D;
import javafx.scene.input.KeyCode;
import javafx.scene.paint.Color;
import javafx.scene.text.Text;

import java.util.Map;

import static com.almasb.fxgl.dsl.FXGL.*;

// 1. Define the types of things in our game
enum MarioType {
    MARIO, GROUND, PLATFORM, GOOMBA, COIN, WALL, EXIT, FLOWER, MUSHROOM
}

public class MarioGame extends GameApplication {

    private Entity player;

    @Override
    protected void initSettings(GameSettings settings) {
        settings.setWidth(1000);
        settings.setHeight(495);
        settings.setTitle("Mario Game Port");
        settings.setVersion("1.0");
        settings.setMainMenuEnabled(true); // Fixes "setMenuEnabled" error
    }

    @Override
    protected void initInput() {
        getInput().addAction(new UserAction("Move Right") {
            @Override
            protected void onAction() {
                player.getComponent(PhysicsComponent.class).setVelocityX(200);
                player.getScaleX(); // check direction
                player.setScaleX(1); // face right
            }
            @Override
            protected void onActionEnd() {
                player.getComponent(PhysicsComponent.class).setVelocityX(0);
            }
        }, KeyCode.RIGHT);

        getInput().addAction(new UserAction("Move Left") {
            @Override
            protected void onAction() {
                player.getComponent(PhysicsComponent.class).setVelocityX(-200);
                player.setScaleX(-1); // face left
            }
            @Override
            protected void onActionEnd() {
                player.getComponent(PhysicsComponent.class).setVelocityX(0);
            }
        }, KeyCode.LEFT);

        getInput().addAction(new UserAction("Jump") {
            @Override
            protected void onActionBegin() {
                PhysicsComponent physics = player.getComponent(PhysicsComponent.class);
                if (physics.isOnGround()) {
                    physics.setVelocityY(-500);
                    play("jump.wav");
                }
            }
        }, KeyCode.UP);
    }

    @Override
    protected void initGameVars(Map<String, Object> vars) {
        vars.put("score", 0);
    }

    @Override
    protected void initGame() {
        getGameWorld().addEntityFactory(new MarioFactory());

        // Set up the background color
        getGameScene().setBackgroundColor(Color.rgb(116, 147, 246)); // Mario Blue

        // Translate the Python map to Java
        String[] map = {
            "b    h      h     h                                                                                                                                                    ",
            "b                                                                                                                                                                      ",
            "b                                                                                                                                                                      ",
            "b                                                                                                                                                                      ",
            "b                                                                                                                                                                      ",
            "b                                                                                                                                                                      ",
            "b                                                                             g  g                                                                                     ",
            "b          ...u..     .?.                                                    .........                                     s                                           ",
            "b  m                                                                                                                      ss                                           ",
            "b                    .                        ..  .                                                                      sss                                           ",
            "b                   ...                      ...  ..                      .f.                                           ssss                                           ",
            "b               ...   ..                    ....  ...                                                                  sssss           c                               ",
            "b    h                                     .....  ....         ?????                                                  ssssss                                           ",
            "b  t =      ==g    p      ==g     =       ......  .....                                                   gg         sssssss       l   #                               ",
            "b-----------------------------------------------  --------------------  -------------   -------------------------------------------------------------------------------",
            "b-----------------------------------------------  --------------------  -------------   -------------------------------------------------------------------------------",
            "b-----------------------------------------------  --------------------  -------------   -------------------------------------------------------------------------------"
        };

        int size = 30;
        int startY = 0; // Adjust if needed based on screen height

        for (int y = 0; y < map.length; y++) {
            String row = map[y];
            for (int x = 0; x < row.length(); x++) {
                char c = row.charAt(x);
                int spawnX = x * size;
                int spawnY = startY + (y * size);

                if (c == '-') spawn("ground", spawnX, spawnY);
                else if (c == '=') spawn("platform", spawnX, spawnY);
                else if (c == 'm') player = spawn("mario", spawnX, spawnY - 10);
                else if (c == 'g') spawn("goomba", spawnX, spawnY);
                else if (c == '?') spawn("coin", spawnX, spawnY); // Simplified for now
                else if (c == '.') spawn("wall", spawnX, spawnY);
                else if (c == 'c') spawn("exit", spawnX, spawnY);
                // Add other mappings here as needed
            }
        }

        // Camera follows player
        Viewport viewport = getGameScene().getViewport();
        viewport.bindToEntity(player, getAppWidth() / 2.0, getAppHeight() / 2.0);
        viewport.setBounds(0, 0, 3000 * 30, getAppHeight()); // Limit camera bounds
        
        // Start music
        loopBGM("mario-theme.ogg");
    }

    @Override
    protected void initPhysics() {
        // Mario vs Coin
        onCollisionBegin(MarioType.MARIO, MarioType.COIN, (mario, coin) -> {
            coin.removeFromWorld();
            inc("score", 1);
            play("coin-sound.wav");
        });

        // Mario vs Goomba
        onCollisionBegin(MarioType.MARIO, MarioType.GOOMBA, (mario, goomba) -> {
            // Simple check: if Mario is falling (moving down), he stomps the Goomba
            if (mario.getComponent(PhysicsComponent.class).getVelocityY() > 0) {
                goomba.removeFromWorld();
                play("stomp.wav");
                mario.getComponent(PhysicsComponent.class).setVelocityY(-300); // Bounce
            } else {
                // Game Over logic
                play("game-over.wav");
                showMessage("Game Over!", () -> getGameController().startNewGame());
            }
        });

        // Mario vs Exit
        onCollisionBegin(MarioType.MARIO, MarioType.EXIT, (mario, exit) -> {
            play("mario-win.mp3");
            showMessage("You Win!", () -> getGameController().startNewGame());
        });
    }

    @Override
    protected void initUI() {
        Text scoreText = new Text();
        scoreText.setTranslateX(50);
        scoreText.setTranslateY(50);
        scoreText.textProperty().bind(getWorldProperties().intProperty("score").asString("Score: %d"));
        scoreText.setStyle("-fx-font-size: 24; -fx-fill: white; -fx-stroke: black; -fx-stroke-width: 1;");
        getGameScene().addUINode(scoreText);
    }

    public static void main(String[] args) {
        launch(args);
    }

    // --- Factory Class inside the same file for simplicity ---
    public static class MarioFactory implements EntityFactory {

        @Spawns("mario")
        public Entity newMario(SpawnData data) {
            PhysicsComponent physics = new PhysicsComponent();
            physics.setBodyType(BodyType.DYNAMIC);
            physics.addGroundSensor(new HitBox("GROUND_SENSOR", new Point2D(5, 30), BoundingShape.box(20, 5)));
            
            // Fix bouncing to stop him from sliding forever
            FixtureDef fd = new FixtureDef();
            fd.setFriction(1.5f); 
            physics.setFixtureDef(fd);

            return entityBuilder(data)
                    .type(MarioType.MARIO)
                    .viewWithBBox("mario1.png")
                    .with(physics)
                    .with(new CollidableComponent(true))
                    .zIndex(10)
                    .build();
        }

        @Spawns("ground")
        public Entity newGround(SpawnData data) {
            return entityBuilder(data)
                    .type(MarioType.GROUND)
                    .viewWithBBox("ground.png")
                    .with(new PhysicsComponent()) // Static by default
                    .build();
        }

        @Spawns("platform")
        public Entity newPlatform(SpawnData data) {
            return entityBuilder(data)
                    .type(MarioType.PLATFORM)
                    .viewWithBBox("ground.png") // reusing ground texture for now
                    .with(new PhysicsComponent())
                    .build();
        }

        @Spawns("wall")
        public Entity newWall(SpawnData data) {
            return entityBuilder(data)
                    .type(MarioType.WALL)
                    .viewWithBBox("mario-brick.png")
                    .with(new PhysicsComponent())
                    .build();
        }

        @Spawns("goomba")
        public Entity newGoomba(SpawnData data) {
            PhysicsComponent physics = new PhysicsComponent();
            physics.setBodyType(BodyType.DYNAMIC);
            
            return entityBuilder(data)
                    .type(MarioType.GOOMBA)
                    .viewWithBBox("goomba.png")
                    .with(physics)
                    .with(new CollidableComponent(true))
                    .build();
        }

        @Spawns("coin")
        public Entity newCoin(SpawnData data) {
            return entityBuilder(data)
                    .type(MarioType.COIN)
                    .viewWithBBox("coin2.png")
                    .with(new CollidableComponent(true))
                    .build();
        }

        @Spawns("exit")
        public Entity newExit(SpawnData data) {
            return entityBuilder(data)
                    .type(MarioType.EXIT)
                    .viewWithBBox("mario-castle.png")
                    .with(new CollidableComponent(true))
                    .scale(0.5, 0.5) // Castle is big
                    .build();
        }
    }
}