from typing import List, Any


class ScalingManager:
    """
    A manager for scaling widgets in the application.

    This class keeps track of registered child objects and provides methods to update their sizes.
    """

    # List to keep track of all registered child objects
    registered_widgets: List[Any] = []

    @staticmethod
    def update_scaling() -> None:
        """
        Updates the scaling of all registered widgets.

        This method triggers the update of sizes for all registered widgets.
        """
        ScalingManager.update_widgets_sizes()

    @staticmethod
    def update_widgets_sizes() -> None:
        """
        Updates the sizes of all registered widgets.

        This method iterates through all registered widgets and updates their sizes.
        """
        for widget in ScalingManager.registered_widgets:
            try:
                widget.reset_size()
            except Exception as error:
                print(f"ScalingManager: Error updating widget size - {error}")

    @staticmethod
    def register_widget(widget: Any) -> None:
        """
        Registers a widget for scaling.

        Args:
            widget: The widget to register for scaling.
        """
        ScalingManager.registered_widgets.append(widget)

    @staticmethod
    def unregister_widget(widget: Any) -> None:
        """
        Unregisters a widget from scaling.

        Args:
            widget: The widget to unregister from scaling.
        """
        ScalingManager.registered_widgets.remove(widget)
