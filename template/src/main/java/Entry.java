package {{PACKAGE_NAME}};

import net.minecraftforge.eventbus.api.SubscribeEvent;
import net.minecraftforge.fml.ModLoadingContext;
import net.minecraftforge.fml.common.Mod;

@Mod.EventBusSubscriber(bus = Mod.EventBusSubscriber.Bus.MOD)
@Mod({{CLASS_NAME}}.ID)
public class {{CLASS_NAME}}
{
    public static final String ID = "{{MOD_ID}}";
}
